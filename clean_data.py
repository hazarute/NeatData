

import sys

if len(sys.argv) > 1 and sys.argv[1] == "--gui":
    from neatdata_gui import NeatDataGUI
    app = NeatDataGUI()
    app.mainloop()
else:
    from modules.cli_handler import main
    main()
