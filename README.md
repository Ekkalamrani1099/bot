# Sistem Requirements
- 2–4 core CPU  
- 4–8GB RAM (lebih ringan dari Ollama)

# Fitur
- auto chat with AI (ChatGPT / GPT-5.2)
- random tag username chat
- auto restart (fix some bug)
- random time spam
- Untuk Push level Discord
- AI lebih manusiawi (GPT-5.2)

**buat screen**

**Install Script**
```
git clone https://github.com/yonarebahan/Discord-auto-with-AI.git
cd Discord-auto-with-AI
```
Buat environtment
```
python3 -m venv dc
source dc/bin/activate
```
**install bahan**
```
pip3 install -r requirements.txt
```
```
pip uninstall discord discord.py discord.py-self -y
```
```
pip install git+https://github.com/dolfies/discord.py-self@71609f4f62649d18bdf14f0e286b7e62bc605390

```
pip install openai
```
**buka script**
```
nano bot.py
```
= isi TOKEN DC & channel ID target (tutorial token : https://www.youtube.com/watch?v=zyl6VGTJ4fY)

= ganti interval min dan max ( untuk waktu random dalam menit )

= klik ctrl + x -> klik y -> klik enter (untuk keluar)

**Mainkan script**
```
python3 bot.py


