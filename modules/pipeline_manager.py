# Merkezi pipeline yönetimi için sınıf ve yardımcı fonksiyonlar
import logging
import toml

class PipelineManager:
	def __init__(self, config_path=None):
		self.steps = []
		self.logger = logging.getLogger("PipelineManager")
		if config_path:
			self.load_config(config_path)

	def add_step(self, step_func, kwargs=None):
		self.steps.append((step_func, kwargs or {}))
		self.logger.info(f"Adım eklendi: {step_func.__name__}")

	def remove_step(self, step_func):
		self.steps = [(func, kw) for func, kw in self.steps if func != step_func]
		self.logger.info(f"Adım çıkarıldı: {step_func.__name__}")

	def run(self, df):
		print("\n--- PIPELINE BAŞLATILDI ---")
		for idx, step in enumerate(self.steps):
			if callable(step[0]):
				func, kwargs = step
				print(f"Adım {idx+1}: {func.__name__} | Parametreler: {kwargs}")
				try:
					before = df.copy()
					df = func(df, **kwargs)
					# Hücre değişimi sayısı
					changed = (before != df).sum().sum() if hasattr(df, 'sum') else '-'
					print(f"Adım sonrası değişen hücre sayısı: {changed}")
				except Exception as e:
					print(f"Adımda hata: {func.__name__} - {e}")
			elif isinstance(step[0], str):
				import importlib
				module_name = step[0]
				params = step[1]
				print(f"Adım {idx+1}: {module_name} | Parametreler: {params}")
				try:
					module = importlib.import_module(f"modules.{module_name}")
					if hasattr(module, "process"):
						before = df.copy()
						df = module.process(df, **params)
						changed = (before != df).sum().sum() if hasattr(df, 'sum') else '-'
						print(f"Adım sonrası değişen hücre sayısı: {changed}")
					else:
						print(f"Modül '{module_name}' içinde 'process' fonksiyonu yok.")
				except Exception as e:
					print(f"Modül '{module_name}' çalıştırılırken hata: {e}")
		print("--- PIPELINE BİTTİ ---\n")
		return df

	def load_config(self, config_path):
		import importlib
		try:
			config = toml.load(config_path)
			steps = config.get("pipeline", {}).get("steps", [])
			self.steps = []
			for step in steps:
				module_name = step["module"]
				params = step.get("params", {})
				try:
					module = importlib.import_module(f"modules.{module_name}")
					if hasattr(module, "process"):
						self.steps.append((module.process, params))
						self.logger.info(f"Pipeline adımı eklendi: {module_name}")
					else:
						self.logger.warning(f"Modül '{module_name}' içinde 'process' fonksiyonu yok, adım atlanıyor.")
				except Exception as e:
					self.logger.warning(f"Modül '{module_name}' yüklenemedi: {e}, adım atlanıyor.")
			self.logger.info(f"Pipeline config loaded from {config_path}")
		except Exception as e:
			self.logger.error(f"Failed to load pipeline config: {e}")

	def set_steps(self, steps):
		self.steps = steps
		self.logger.info("Pipeline adımları güncellendi.")

# Örnek modül arayüzü: Tüm modüller process(df, **kwargs) şeklinde olmalı
# def process(df, **kwargs):
#     ...
#     return df
