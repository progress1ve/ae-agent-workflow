import importlib.util,json,subprocess,sys,tempfile,unittest
from pathlib import Path
import numpy as np
import soundfile as sf
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
def module(path):
 spec=importlib.util.spec_from_file_location(path.stem,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
audio=module(ROOT/'audio/audio_ops.py');installer=module(ROOT/'scripts/install.py')

class Helpers(unittest.TestCase):
 def test_timeline_relative_paths_duration_and_ceiling(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);sf.write(p/'cue.wav',np.sin(np.arange(24000)*.07)*.8,24000)
   plan={'duration':1,'cues':[{'file':'cue.wav','time':.2,'length':.5,'peak_db':-1}]};(p/'plan.json').write_text(json.dumps(plan))
   result=audio.render(p/'plan.json',p/'nested/out.wav');x,sr=sf.read(p/'nested/out.wav')
   self.assertEqual(sr,48000);self.assertEqual(x.shape,(48000,2));self.assertLessEqual(abs(x).max(),10**(-2/20)+1e-6);self.assertLess(np.abs(x[:9000]).max(),1e-7);self.assertGreater(np.abs(x[12000:20000]).max(),.01)
 def test_bad_cue_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'bad.json';p.write_text(json.dumps({'duration':1,'cues':[{'file':'missing.wav','time':-1,'length':.1,'peak_db':-10}]}))
   with self.assertRaises(ValueError):audio.render(p,Path(d)/'out.wav')
 def test_skill_update_preserves_user_files(self):
  with tempfile.TemporaryDirectory() as d:
   target=Path(d)/'skill';installer.install_skill(target);(target/'user-note.txt').write_text('retain')
   with self.assertRaises(ValueError):installer.install_skill(target)
   installer.install_skill(target,update=True);self.assertEqual((target/'user-note.txt').read_text(),'retain')
 def test_mcp_handshake_and_tool_call(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'test.wav';sf.write(p,np.zeros(4800),48000)
   requests=[{'jsonrpc':'2.0','id':1,'method':'initialize','params':{'protocolVersion':'2024-11-05'}},{'jsonrpc':'2.0','method':'notifications/initialized'},{'jsonrpc':'2.0','id':2,'method':'tools/list'},{'jsonrpc':'2.0','id':3,'method':'tools/call','params':{'name':'inspect_audio','arguments':{'files':[str(p)]}}}]
   run=subprocess.run([sys.executable,str(ROOT/'audio/server.py')],input=''.join(json.dumps(q)+'\n' for q in requests),text=True,capture_output=True,check=True)
   answers=[json.loads(line) for line in run.stdout.splitlines()];self.assertEqual([q['id'] for q in answers],[1,2,3]);self.assertEqual(len(answers[1]['result']['tools']),3);self.assertFalse(answers[2]['result']['isError']);data=json.loads(answers[2]['result']['content'][0]['text']);self.assertAlmostEqual(data[0]['seconds'],.1)
 def test_alpha_chroma_encoding(self):
  with tempfile.TemporaryDirectory() as d:
   p=Path(d);frames=p/'frames';frames.mkdir()
   for i in range(3):
    im=Image.new('RGBA',(64,32),(0,0,0,0));im.paste((20,90,180,255),(20,10,45,25));im.save(frames/f'frame_{i:06d}.png')
   (frames/'complete.json').write_text(json.dumps({'frames':3,'fps':30,'width':64,'height':32}))
   subprocess.run([sys.executable,str(ROOT/'scripts/encode_frames.py'),'--frames',str(frames),'--fps','30','--out',str(p/'demo')],check=True,capture_output=True)
   import imageio_ffmpeg
   raw=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(p/'demo-alpha.mov'),'-frames:v','1','-f','rawvideo','-pix_fmt','rgba','pipe:1'],stdout=subprocess.PIPE,check=True).stdout
   arr=np.frombuffer(raw,np.uint8).reshape(32,64,4);self.assertEqual(arr[0,0,3],0);self.assertEqual(arr[15,30,3],255)

if __name__=='__main__':unittest.main()
