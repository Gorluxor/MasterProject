from subprocess_input_streamer import SubprocessInputStreamer
import subprocess
python3_command = "python2 ..\\reldi-tagger-master\\tagger.py -l sr"
sis = SubprocessInputStreamer(python3_command.split(), popen_kwargs=
    {
    'stdin': subprocess.PIPE,
    'stdout': subprocess.PIPE,
    }
)
with sis, open('text.txt', 'rb') as f:
    while True:
        data = f.read(1024)
        if not data:
            break
        sis.write(data)
assert sis.exit_code == 0
print(sis.stdout.decode())