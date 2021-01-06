const { exec } = require("child_process");

exec(
	"pip install -r requirements.txt && python3 manage.py runserver 0.0.0.0:%PORT%",
	(error, stdout, stderr) => {
		if (stdout) {
			console.log(`error: ${stdout}`);
			return;
		}
		if (error) {
			console.log(`error: ${error.message}`);
			return;
		}
		if (stderr) {
			console.log(`stderr: ${stderr}`);
			return;
		}
		console.log(`stdout: ${stdout}`);
	}
);
