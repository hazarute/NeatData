import tkinter as tk
from tkinter import filedialog, messagebox

class NeatDataGUI(tk.Tk):
	def __init__(self):
		super().__init__()
		self.title('NeatData - CSV Cleaner')
		self.geometry('700x500')
		self.create_widgets()

	def create_widgets(self):
		# Dosya seçimi
		self.file_label = tk.Label(self, text='CSV Dosyası Seç:')
		self.file_label.pack(pady=5)
		self.file_button = tk.Button(self, text='Dosya Seç', command=self.select_file)
		self.file_button.pack(pady=5)
		self.selected_file = tk.StringVar()
		self.file_entry = tk.Entry(self, textvariable=self.selected_file, width=60)
		self.file_entry.pack(pady=5)

		# Temizleme seçenekleri paneli (örnek)
		self.options_frame = tk.LabelFrame(self, text='Temizleme Seçenekleri')
		self.options_frame.pack(fill='x', padx=10, pady=10)
		self.dropna_var = tk.BooleanVar()
		self.dropna_check = tk.Checkbutton(self.options_frame, text='Eksik Satırları Sil (--dropna)', variable=self.dropna_var)
		self.dropna_check.pack(anchor='w')
		self.fillna_var = tk.BooleanVar()
		self.fillna_check = tk.Checkbutton(self.options_frame, text='Eksik Değerleri Doldur (--fillna)', variable=self.fillna_var)
		self.fillna_check.pack(anchor='w')
		self.textcol_var = tk.StringVar()
		self.textcol_label = tk.Label(self.options_frame, text='Metin Sütunu (--textcol):')
		self.textcol_label.pack(anchor='w')
		self.textcol_entry = tk.Entry(self.options_frame, textvariable=self.textcol_var)
		self.textcol_entry.pack(anchor='w')

		# İlerleme çubuğu
		self.progress = tk.DoubleVar()
		self.progress_bar = tk.Scale(self, variable=self.progress, from_=0, to=100, orient='horizontal', length=400, label='İlerleme')
		self.progress_bar.pack(pady=10)

		# Çıktı ayarları
		self.output_frame = tk.LabelFrame(self, text='Çıktı Ayarları')
		self.output_frame.pack(fill='x', padx=10, pady=10)
		self.output_format = tk.StringVar(value='Excel')
		self.excel_radio = tk.Radiobutton(self.output_frame, text='Excel', variable=self.output_format, value='Excel')
		self.excel_radio.pack(side='left', padx=5)
		self.csv_radio = tk.Radiobutton(self.output_frame, text='CSV', variable=self.output_format, value='CSV')
		self.csv_radio.pack(side='left', padx=5)
		self.output_dir = tk.StringVar()
		self.output_dir_button = tk.Button(self.output_frame, text='Çıktı Dizini Seç', command=self.select_output_dir)
		self.output_dir_button.pack(side='left', padx=5)
		self.output_dir_entry = tk.Entry(self.output_frame, textvariable=self.output_dir, width=40)
		self.output_dir_entry.pack(side='left', padx=5)

		# Başlat/Durdur butonları
		self.start_button = tk.Button(self, text='Temizlemeyi Başlat', command=self.run_cleaning)
		self.start_button.pack(pady=10)
		self.stop_button = tk.Button(self, text='Durdur', command=self.stop_cleaning)
		self.stop_button.pack(pady=5)

		# Konsol/log alanı
		self.log_text = tk.Text(self, height=8, width=80)
		self.log_text.pack(pady=10)

	def select_file(self):
		file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
		if file_path:
			self.selected_file.set(file_path)

	def select_output_dir(self):
		dir_path = filedialog.askdirectory()
		if dir_path:
			self.output_dir.set(dir_path)

	def run_cleaning(self):
		import threading
		self.log_text.insert(tk.END, 'Temizleme işlemi başlatıldı...\n')
		def process():
			import os
			import pandas as pd
			from modules.pipeline_manager import PipelineManager
			# Dosya yolu
			file_path = self.selected_file.get()
			if not file_path:
				self.log_text.insert(tk.END, 'Lütfen bir CSV dosyası seçin.\n')
				return
			try:
				# Dosya okuma
				ext = os.path.splitext(file_path)[-1].lower()
				if ext == ".csv":
					import chardet, csv
					def detect_encoding_and_delimiter(filename, sample_size=4096):
						with open(filename, 'rb') as f:
							raw = f.read(sample_size)
							result = chardet.detect(raw)
							encoding = result['encoding']
						with open(filename, 'r', encoding=encoding, errors='replace') as f:
							sample = f.read(sample_size)
							sniffer = csv.Sniffer()
							try:
								dialect = sniffer.sniff(sample)
								delimiter = dialect.delimiter
							except Exception:
								delimiter = ','
						return encoding, delimiter
					encoding, delimiter = detect_encoding_and_delimiter(file_path)
					df = pd.read_csv(file_path, encoding=encoding, sep=delimiter)
				elif ext in [".xlsx", ".xlsm", ".xls"]:
					df = pd.read_excel(file_path)
				else:
					self.log_text.insert(tk.END, f"Desteklenmeyen dosya formatı: {ext}\n")
					return
				self.log_text.insert(tk.END, f"{file_path} başarıyla okundu. Satır sayısı: {len(df)}\n")
				# PipelineManager ile temizlik
				config_path = "modules/pipeline_config.toml"
				manager = PipelineManager(config_path=config_path)
				# Seçenekler
				if self.dropna_var.get():
					from modules.handle_missing_values import process as handle_missing_process
					manager.add_step(handle_missing_process, {"method": "drop"})
				elif self.fillna_var.get():
					from modules.handle_missing_values import process as handle_missing_process
					fill_value = self.textcol_var.get() if self.textcol_var.get() else ""
					manager.add_step(handle_missing_process, {"method": "fill", "fill_value": fill_value})
				if self.textcol_var.get():
					from modules.standardize_text_column import process as standardize_text_process
					manager.add_step(standardize_text_process, {"column": self.textcol_var.get()})
				from modules.remove_duplicates_report import process as remove_duplicates_process
				manager.add_step(remove_duplicates_process)
				# Temizlik işlemi
				before = len(df)
				df = manager.run(df)
				tekrar_silinen = before - len(df)
				self.log_text.insert(tk.END, f"Tekrar eden satır silinen: {tekrar_silinen}\n")
				# Çıktı dosyası
				output_dir = self.output_dir.get() or os.path.dirname(file_path)
				input_base = os.path.splitext(os.path.basename(file_path))[0].replace(' ', '_')
				output_format = self.output_format.get()
				if output_format == "Excel":
					output_file = os.path.join(output_dir, f"cleaned_{input_base}.xlsx")
					from modules.save_to_excel import process as save_to_excel_process
					save_to_excel_process(df, output_file=output_file)
				else:
					output_file = os.path.join(output_dir, f"cleaned_{input_base}.csv")
					df.to_csv(output_file, index=False)
				self.log_text.insert(tk.END, f"Temizlenmiş veri '{output_file}' dosyasına kaydedildi.\n")
				self.progress.set(100)
			except Exception as e:
				self.log_text.insert(tk.END, f"Hata: {e}\n")
		threading.Thread(target=process).start()

	def stop_cleaning(self):
		self.log_text.insert(tk.END, 'İşlem durduruldu.\n')

if __name__ == '__main__':
	app = NeatDataGUI()
	app.mainloop()