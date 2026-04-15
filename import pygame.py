import pygame
import random
import sys
import json
import math

# ═══════════════════════════════════════════════════════════════
#  INICIALIZAÇÃO
# ═══════════════════════════════════════════════════════════════
pygame.init()
LARGURA_TELA = 800
ALTURA_TELA  = 650
CHAO_Y       = 543   # y onde o chão visual do fundo.jpg começa
FPS          = 60
tela  = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
clock = pygame.time.Clock()
pygame.display.set_caption("Fúria das Masmorras")

# ═══════════════════════════════════════════════════════════════
#  CORES
# ═══════════════════════════════════════════════════════════════
PRETO   = (  0,   0,   0);  BRANCO  = (255, 255, 255)
VERM    = (220,  30,  30);  VERDE   = ( 30, 200,  30)
AMAR    = (255, 215,   0);  LARAN   = (255, 140,   0)
CINZA   = ( 80,  80,  80);  AZUL    = ( 50, 100, 220)
ROXO    = (150,  50, 200);  CIANO   = ( 50, 200, 200)
ROSA    = (220,  80, 120);  MARROM  = (120,  60,  20)
DOURO   = (218, 165,  32);  CARVAO  = ( 30,  30,  30)

# ═══════════════════════════════════════════════════════════════
#  FONTES
# ═══════════════════════════════════════════════════════════════
FG = pygame.font.Font(None, 74)
FM = pygame.font.Font(None, 48)
FP = pygame.font.Font(None, 36)
FI = pygame.font.Font(None, 24)

# ═══════════════════════════════════════════════════════════════
#  SPRITES PROCEDURAIS
# ═══════════════════════════════════════════════════════════════
def _ns(w, h): return pygame.Surface((w, h), pygame.SRCALPHA)

def _hum(s, cc, cp):
    w, h = s.get_width(), s.get_height()
    pygame.draw.ellipse(s, cp, (int(w*.32), int(h*.02), int(w*.36), int(h*.24)))
    bx,by,bw,bh = int(w*.27),int(h*.26),int(w*.46),int(h*.34)
    pygame.draw.rect(s, cc, (bx,by,bw,bh))
    pygame.draw.rect(s, cc, (bx-int(w*.14), by, int(w*.14), int(bh*.75)))
    pygame.draw.rect(s, cc, (bx+bw, by, int(w*.14), int(bh*.75)))
    lw = int(bw*.42)
    leg_top = by+bh
    # pernas estendem até o fim do sprite para encostar no chão
    pygame.draw.rect(s, cc, (bx, leg_top, lw, h-leg_top))
    pygame.draw.rect(s, cc, (bx+bw-lw, leg_top, lw, h-leg_top))
    # pés
    pygame.draw.rect(s, cp, (bx-2, h-6, lw+4, 6))
    pygame.draw.rect(s, cp, (bx+bw-lw-2, h-6, lw+4, 6))
    pygame.draw.circle(s, PRETO, (int(w*.42), int(h*.10)), 2)
    pygame.draw.circle(s, PRETO, (int(w*.58), int(h*.10)), 2)

def _sp_guerreiro():
    s = _ns(64,80); _hum(s,(160,100,30),(210,160,100))
    pygame.draw.rect(s,DOURO,(17,21,30,7))
    pygame.draw.rect(s,(180,130,30),(19,2,26,6)); return s

def _sp_mago():
    """Usa personagem.png com tinte azul/roxo — mesma qualidade de sprite."""
    try:
        s = pygame.image.load("personagem.png").convert_alpha()
        tint = pygame.Surface(s.get_size()); tint.fill((95, 80, 255))
        s.blit(tint,(0,0),special_flags=pygame.BLEND_RGB_MULT)
        # Brilho arcano: leve overlay ciano no topo (capuz)
        glow = pygame.Surface(s.get_size(),pygame.SRCALPHA)
        pygame.draw.ellipse(glow,(80,40,200,60),(s.get_width()//4,0,s.get_width()//2,s.get_height()//3))
        s.blit(glow,(0,0)); return s
    except:
        s = _ns(64,80); _hum(s,(55,40,140),(195,165,220)); return s

def _sp_ladino():
    """Usa personagem.png com tinte escuro/esverdeado — mesmo nível visual."""
    try:
        s = pygame.image.load("personagem.png").convert_alpha()
        tint = pygame.Surface(s.get_size()); tint.fill((75, 110, 80))
        s.blit(tint,(0,0),special_flags=pygame.BLEND_RGB_MULT)
        # Sombra nas bordas (visual furtivo)
        shadow = pygame.Surface(s.get_size(),pygame.SRCALPHA)
        pygame.draw.ellipse(shadow,(0,0,0,80),(0,0,s.get_width()//3,s.get_height()))
        pygame.draw.ellipse(shadow,(0,0,0,60),(s.get_width()*2//3,0,s.get_width()//3,s.get_height()))
        s.blit(shadow,(0,0)); return s
    except:
        s = _ns(64,80); _hum(s,(40,38,48),(155,125,95)); return s

def _sp_velhobarbudo():
    """Sprite procedural de fallback para o Velho Barbudo."""
    s = _ns(64,80); _hum(s,(80,68,100),(200,185,165))
    # barba branca
    pygame.draw.ellipse(s,(230,230,230),(20,34,24,20))
    # chapéu pontudo
    pygame.draw.polygon(s,(55,40,90),[(32,2),(18,26),(46,26)])
    return s

def _sp_ini_base(tipo):
    """Sprites fallback para inimigos 1-12 (caso PNG não exista)."""
    paletas = [
        ((80,50,30),(150,90,60)),    # 1 goblin
        ((40,100,50),(80,160,90)),   # 2 goblin verde
        ((60,60,80),(180,175,170)),  # 3 esqueleto
        ((100,40,40),(160,80,80)),   # 4 orc
        ((50,30,100),(120,90,180)),  # 5 elfo negro
        ((120,80,20),(190,150,70)),  # 6 lagarto
        ((30,80,90),(80,160,170)),   # 7 troll
        ((80,30,80),(150,80,150)),   # 8 demônio
        ((60,60,30),(130,130,60)),   # 9 zumbi
        ((35,35,35),(90,90,90)),     # 10 sombra
        ((140,60,20),(210,110,50)),  # 11 guerreiro fogo
        ((20,60,110),(60,130,200)),  # 12 guerreiro gelo
    ]
    cc, cp = paletas[max(0, tipo-1) % 12]
    s = _ns(48, 62); _hum(s, cc, cp)
    # detalhe extra por tipo
    if tipo == 3:  # esqueleto: olhos brilhantes
        pygame.draw.circle(s, VERM, (17, 8), 3)
        pygame.draw.circle(s, VERM, (31, 8), 3)
    elif tipo == 4:  # orc: presas
        pygame.draw.polygon(s, BRANCO, [(19,22),(21,22),(20,28)])
        pygame.draw.polygon(s, BRANCO, [(27,22),(29,22),(28,28)])
    elif tipo == 6:  # lagarto: cauda
        pygame.draw.arc(s, cc, (34, 38, 20, 18), 0, math.pi, 3)
    elif tipo == 8:  # demônio: chifres
        pygame.draw.polygon(s, (80,0,0), [(14,2),(10,0),(16,8)])
        pygame.draw.polygon(s, (80,0,0), [(34,2),(38,0),(32,8)])
    elif tipo == 11:  # guerreiro fogo
        pygame.draw.circle(s, LARAN, (24, 4), 5)
    elif tipo == 12:  # guerreiro gelo
        pygame.draw.polygon(s, CIANO, [(20,3),(28,3),(24,0)])
    return s

def _sp_ini_novo(tipo):
    configs = {
        13:((50,65),(30,130,30),(100,180,80)),
        14:((60,70),(180,80,20),(220,140,60)),
        15:((45,50),(220,50,150),(240,120,180)),
        16:((48,62),(140,180,220),(200,220,240)),
        17:((55,68),(200,30,30),(230,100,80)),
        18:((80,100),(100,60,20),(180,120,60)),
        19:((50,65),(20,160,80),(120,200,140)),
        20:((44,60),(60,20,80),(120,80,140)),
        21:((58,72),(100,100,120),(160,160,180)),
        22:((52,68),(180,200,160),(220,230,200)),
    }
    (w,h),cc,cp = configs.get(tipo,((50,65),CINZA,BRANCO))
    s = _ns(w,h)
    if tipo == 16:
        pygame.draw.ellipse(s,cc+(160,),(4,4,w-8,h-8))
        pygame.draw.ellipse(s,cp+(200,),(w//4,h//8,w//2,h//3))
    else:
        _hum(s,cc,cp)
        if tipo==13: pygame.draw.arc(s,MARROM,(int(w*.62),int(h*.22),14,28),0,math.pi,3)
        elif tipo==19:
            cx,cy=w//2,int(h*.37)
            pygame.draw.line(s,BRANCO,(cx-6,cy),(cx+6,cy),2)
            pygame.draw.line(s,BRANCO,(cx,cy-6),(cx,cy+6),2)
        elif tipo==21:
            pygame.draw.polygon(s,(100,100,140),[(2,int(h*.20)),(int(w*.22),int(h*.16)),(int(w*.22),int(h*.62)),(2,int(h*.62))])
        elif tipo==22:
            ex,ey=w//2,int(h*.10)
            pygame.draw.line(s,VERM,(ex-5,ey-4),(ex+5,ey+4),2)
            pygame.draw.line(s,VERM,(ex+5,ey-4),(ex-5,ey+4),2)
    return s

def _sp_boss(idx):
    w,h=100,120; s=_ns(w,h)
    if idx==0:  # Dragão
        pygame.draw.ellipse(s,(180,30,20),(10,30,80,70))
        pygame.draw.ellipse(s,(200,50,30),(52,8,48,40))
        pygame.draw.polygon(s,(150,20,15),[(10,35),(0,2),(30,26)])
        pygame.draw.polygon(s,(150,20,15),[(70,35),(98,2),(70,26)])
        pygame.draw.circle(s,AMAR,(72,24),5); pygame.draw.circle(s,PRETO,(74,24),2)
        pygame.draw.polygon(s,(200,50,30),[(95,25),(100,38),(92,45)])
    elif idx==1:  # Cavaleiro Sombrio
        _hum(s,(20,20,30),(50,50,60))
        pygame.draw.rect(s,(30,30,42),(w//4,1,w//2,int(h*.24)))
        pygame.draw.ellipse(s,(42,42,54),(0,int(h*.22),int(w*.28),int(h*.10)))
        pygame.draw.ellipse(s,(42,42,54),(int(w*.72),int(h*.22),int(w*.28),int(h*.10)))
        pygame.draw.rect(s,(180,180,200),(int(w*.82),int(h*.20),5,int(h*.54)))
        pygame.draw.rect(s,(150,100,30),(int(w*.75),int(h*.38),19,6))
        pygame.draw.circle(s,VERM,(int(w*.38),int(h*.11)),4)
        pygame.draw.circle(s,VERM,(int(w*.62),int(h*.11)),4)
    elif idx==2:  # Mago Maligno
        _hum(s,(80,20,120),(180,140,220))
        pygame.draw.polygon(s,(60,10,100),[(w//2,0),(w//2-18,int(h*.18)),(w//2+18,int(h*.18))])
        pygame.draw.circle(s,AMAR,(w//2,4),4)
        pygame.draw.circle(s,(180,50,255),(int(w*.83),int(h*.31)),10)
        pygame.draw.circle(s,(120,0,200),(int(w*.83),int(h*.31)),12,2)
    elif idx==3:  # Lorde Demônio
        _hum(s,(160,20,20),(210,80,60))
        pygame.draw.polygon(s,(120,10,10),[(int(w*.30),int(h*.08)),(int(w*.20),0),(int(w*.40),int(h*.08))])
        pygame.draw.polygon(s,(120,10,10),[(int(w*.70),int(h*.08)),(int(w*.60),int(h*.08)),(int(w*.80),0)])
        pygame.draw.polygon(s,(100,10,10),[(5,int(h*.30)),(0,int(h*.08)),(int(w*.26),int(h*.35))])
        pygame.draw.polygon(s,(100,10,10),[(int(w*.95),int(h*.30)),(w,int(h*.08)),(int(w*.74),int(h*.35))])
        pygame.draw.circle(s,LARAN,(int(w*.38),int(h*.10)),5)
        pygame.draw.circle(s,LARAN,(int(w*.62),int(h*.10)),5)
    else:  # Deus do Caos
        cx,cy=w//2,h//2
        for cor,r in [(BRANCO,46),(PRETO,38),(BRANCO,28),(ROXO,18)]:
            pygame.draw.circle(s,cor,(cx,cy),r)
        for ang in range(0,360,30):
            ax=cx+int(50*math.cos(math.radians(ang))); ay=cy+int(50*math.sin(math.radians(ang)))
            pygame.draw.line(s,AMAR,(cx,cy),(ax,ay),1)
        pygame.draw.circle(s,CIANO,(cx,cy),8)
    return s

def _sp_pocao():
    s=_ns(28,38)
    pygame.draw.rect(s,(180,60,80),(8,0,12,8))
    pygame.draw.ellipse(s,(220,80,100),(2,7,24,28))
    pygame.draw.ellipse(s,(255,150,150),(6,12,8,8)); return s

def _sp_bota():
    s=_ns(32,30)
    pygame.draw.polygon(s,(80,50,20),[(2,16),(2,28),(26,28),(26,22),(18,22),(18,16)])
    pygame.draw.rect(s,(100,65,30),(10,6,12,16))
    pygame.draw.line(s,VERDE,(12,10),(20,10),2); return s

def _sp_bomba():
    s=_ns(30,34)
    pygame.draw.circle(s,(40,40,40),(15,20),14)
    pygame.draw.line(s,CINZA,(15,6),(18,0),2)
    pygame.draw.circle(s,LARAN,(20,1),3)
    pygame.draw.circle(s,(60,60,80),(15,20),8); return s

def _sp_mp10():
    s=_ns(26,26)
    pygame.draw.circle(s,(100,200,255),  (13,13),11)
    pygame.draw.circle(s,(180,235,255),  (10,10), 5)
    pygame.draw.circle(s,(255,255,255),  (10,10), 2)
    return s

def _sp_mp20():
    s=_ns(28,28)
    pygame.draw.circle(s,(50,100,240),   (14,14),12)
    pygame.draw.circle(s,(130,180,255),  (11,11), 5)
    pygame.draw.circle(s,(220,240,255),  (11,11), 2)
    return s

def _sp_mp50():
    s=_ns(30,30)
    pygame.draw.circle(s,(140,60,220),   (15,15),13)
    pygame.draw.circle(s,(210,140,255),  (12,12), 6)
    pygame.draw.circle(s,(240,220,255),  (12,12), 2)
    return s

def _sp_mpfull():
    s=_ns(32,32)
    pygame.draw.circle(s,(220,180,0),    (16,16),14)
    pts=[]
    import math as _m
    for i in range(8):
        r=14 if i%2==0 else 7
        a=_m.radians(i*45-90)
        pts.append((int(16+r*_m.cos(a)),int(16+r*_m.sin(a))))
    pygame.draw.polygon(s,(255,230,50),pts)
    pygame.draw.circle(s,(255,255,200),  (16,16), 5)
    return s

# ═══════════════════════════════════════════════════════════════
#  CARREGAMENTO DE ASSETS
# ═══════════════════════════════════════════════════════════════
def _img(path, fb=None):
    try: return pygame.image.load(path).convert_alpha()
    except: return fb() if fb else _ns(48,60)

def _load_gif(path):
    """Carrega todos os frames de um GIF animado via Pillow.
    Retorna (lista_de_frames, primeira_surface) ou (None, None) se falhar."""
    try:
        from PIL import Image
        gif = Image.open(path)
        frames = []
        try:
            while True:
                dur = max(gif.info.get('duration', 100), 50)
                rgba = gif.convert('RGBA')
                w, h = rgba.size
                surf = pygame.image.fromstring(rgba.tobytes(), (w, h), 'RGBA').convert_alpha()
                frames.append((surf, dur))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass
        if frames:
            return frames, frames[0][0]
    except Exception:
        pass
    return None, None

class GifAnim:
    """Controla a animação de um GIF quadro a quadro."""
    def __init__(self, frames):
        self.frames = frames          # [(surface, duration_ms), ...]
        self.total_ms = sum(d for _, d in frames)
        self._ms = 0
    def tick(self, dt=16):
        self._ms = (self._ms + dt) % self.total_ms
    def current(self):
        t = 0
        for surf, dur in self.frames:
            t += dur
            if self._ms < t:
                return surf
        return self.frames[-1][0]

def _som(path):
    try: return pygame.mixer.Sound(path)
    except: return None

def _load_ck(path, size=None, tol=45):
    """Carrega PNG: flood-fill pelo fundo externo + limpeza de franjas + blobs isolados."""
    try:
        import numpy as np
        from collections import deque, Counter
        raw = pygame.image.load(path).convert()
        w, h = raw.get_size()
        sample = []
        for x in range(0,w,3): sample+=[raw.get_at((x,0))[:3],raw.get_at((x,h-1))[:3]]
        for y in range(0,h,3): sample+=[raw.get_at((0,y))[:3],raw.get_at((w-1,y))[:3]]
        bg = np.array(Counter(sample).most_common(1)[0][0], dtype=np.float32)
        arr = pygame.surfarray.array3d(raw).astype(np.float32)
        dist = np.sqrt(((arr - bg)**2).sum(axis=2))
        is_bg = dist < tol
        visited = np.zeros((w,h), dtype=bool); queue = deque()
        for x in range(w):
            if is_bg[x,0]:   visited[x,0]=True;   queue.append((x,0))
            if is_bg[x,h-1]: visited[x,h-1]=True; queue.append((x,h-1))
        for y in range(h):
            if is_bg[0,y]:   visited[0,y]=True;   queue.append((0,y))
            if is_bg[w-1,y]: visited[w-1,y]=True; queue.append((w-1,y))
        while queue:
            x,y = queue.popleft()
            for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
                if 0<=nx<w and 0<=ny<h and not visited[nx,ny] and is_bg[nx,ny]:
                    visited[nx,ny]=True; queue.append((nx,ny))
        alpha = np.where(visited, 0, 255).astype(np.uint8)
        brightness = arr.mean(axis=2)
        # 1) erode franjas escuras adjacentes ao fundo
        for _ in range(3):
            transp = np.pad(alpha==0, 1, constant_values=False)
            adj = transp[:-2,1:-1]|transp[2:,1:-1]|transp[1:-1,:-2]|transp[1:-1,2:]
            alpha[adj & (alpha==255) & (brightness < 85)] = 0
        # 2) remove blobs isolados menores que 8% do corpo principal
        try:
            from scipy.ndimage import label as _cc
            labeled, num = _cc(alpha==255)
            if num > 0:
                sizes = np.bincount(labeled.ravel())
                max_sz = sizes[1:].max()
                for i in range(1, num+1):
                    if sizes[i] < max(200, max_sz * 0.08):
                        alpha[labeled==i] = 0
        except ImportError: pass
        result = pygame.Surface((w,h), pygame.SRCALPHA)
        pygame.surfarray.blit_array(result, pygame.surfarray.array3d(raw))
        pa = pygame.surfarray.pixels_alpha(result); pa[:]=alpha; del pa
        if size: result = pygame.transform.scale(result, size)
        return result
    except: return None

def _musica(lista, fallback="musica_fundo.mp3"):
    for c in lista:
        try: pygame.mixer.music.load(c); return c
        except: pass
    try: pygame.mixer.music.load(fallback)
    except: pass
    return None

def _imgsc(path, size, fb):
    t = _img(path); return pygame.transform.scale(t, size) if t else fb()
_img_mago   = _imgsc("mago.png",         (76,118), _sp_mago)
_img_ladino = _imgsc("ladino.png",       (76,118), _sp_ladino)
_img_velho  = _imgsc("velhobarbudo.png", (76,118), _sp_velhobarbudo)
imgs_char = [_img("personagem.png", _sp_guerreiro), _img_mago, _img_ladino, _img_velho]
def _ini_fn(i): return "inimigo.png" if i==1 else f"inimigo{i}.png"
_gif_map      = {}  # idx -> GifAnim  (imgs_ini animados)
_gif_boss_map = {}  # idx -> GifAnim  (imgs_boss animados)
_gif_fboss_map= {}  # fi  -> GifAnim  (fboss_imgs animados)

def _ini_img(i, fb):
    idx = i - 1
    fn = "inimigo.gif" if i == 1 else f"inimigo{i}.gif"
    frames, first = _load_gif(fn)
    if frames:
        _gif_map[idx] = GifAnim(frames)
        return first
    return _img(_ini_fn(i), fb)

imgs_ini  = [_ini_img(i, lambda i=i:_sp_ini_base(i)) for i in range(1,13)] + \
            [_ini_img(i, lambda i=i:_sp_ini_novo(i)) for i in range(13,64)]

def _boss_img(i):
    frames, first = _load_gif(f"boss{i+1}.gif")
    if frames:
        _gif_boss_map[i] = GifAnim(frames)
        return first
    return _img(f"boss{i+1}.png", lambda i=i:_sp_boss(i))

imgs_boss = [_boss_img(i) for i in range(5)]
machado       = _img("machado.png")
cajado_img    = _imgsc("cajado.png",      (36,57), lambda: machado)
espada_img    = _imgsc("espada.png",      (34,58), lambda: machado)
machadobarba  = _imgsc("machadobarba.png", (36,57), lambda: machado)
imgs_item = {"pocao":_img("item.png",_sp_pocao), "bota":_img("item_bota.png",_sp_bota), "bomba":_img("item_bomba.png",_sp_bomba),
             "mp10":_sp_mp10(), "mp20":_sp_mp20(), "mp50":_sp_mp50(), "mpfull":_sp_mpfull()}

def _trans_bottom(img):
    """Conta pixels transparentes no fundo do sprite para alinhar ao chão."""
    H = img.get_height()
    for y in range(H-1, -1, -1):
        for x in range(img.get_width()):
            if img.get_at((x, y))[3] > 10:
                return H - 1 - y
    return 0

off_char  = [_trans_bottom(img) for img in imgs_char]
off_ini   = [_trans_bottom(img) for img in imgs_ini]
off_boss  = [_trans_bottom(img) for img in imgs_boss]
off_item_d= {k: _trans_bottom(v) for k, v in imgs_item.items()}

_FBOSS_CFG = [
    ("inimigo13",   (140,115), lambda: _sp_boss(0)),
    ("inimigo14",   (140,115), lambda: _sp_boss(1)),
    ("inimigo15",   (140,108), lambda: _sp_boss(2)),
    ("inimigo16",   (200,155), lambda: _sp_boss(3)),
    ("inimigofinal",(160,130), lambda: _sp_boss(4)),
]
def _fboss_img(fi, name, size, fb):
    frames, first = _load_gif(f"{name}.gif")
    if frames:
        scaled = [(pygame.transform.scale(s, size), d) for s, d in frames]
        _gif_fboss_map[fi] = GifAnim(scaled)
        return scaled[0][0]
    return _imgsc(f"{name}.png", size, fb)
fboss_imgs = [_fboss_img(fi, name, size, fb) for fi,(name,size,fb) in enumerate(_FBOSS_CFG)]
off_fboss = [_trans_bottom(img) for img in fboss_imgs]

_gif_extra_boss_map = {}
_EXTRA_BOSS_CFG = [
    ("bossfinal1",(180,155),lambda:_sp_boss(0)),
    ("bossfinal2",(185,160),lambda:_sp_boss(1)),
    ("bossfinal3",(195,165),lambda:_sp_boss(2)),
    ("bossfinal4",(205,175),lambda:_sp_boss(3)),
    ("bossfinal5",(215,185),lambda:_sp_boss(4)),
]
def _extra_boss_img(fi, name, size, fb):
    frames, first = _load_gif(f"{name}.gif")
    if frames:
        scaled = [(pygame.transform.scale(s, size), d) for s, d in frames]
        _gif_extra_boss_map[fi] = GifAnim(scaled)
        return scaled[0][0]
    return _imgsc(f"{name}.png", size, fb)
extra_boss_imgs = [_extra_boss_img(fi,name,size,fb) for fi,(name,size,fb) in enumerate(_EXTRA_BOSS_CFG)]
off_extra_boss  = [_trans_bottom(img) for img in extra_boss_imgs]

som_atq  = _som("ataque.wav");   som_col  = _som("colisao.wav")
som_pulo = _som("pulo.wav");     som_colt = _som("coleta.wav")
som_bomb = _som("bomba.wav")

def _play(s):
    if s: s.play()

# ═══════════════════════════════════════════════════════════════
#  FUNDOS (5 CENÁRIOS)
# ═══════════════════════════════════════════════════════════════
def _fundo_dungeon():
    try: return pygame.image.load("fundo.jpg").convert()
    except:
        s=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); s.fill((30,25,20))
        for y in range(0,ALTURA_TELA,40): pygame.draw.line(s,(50,40,30),(0,y),(LARGURA_TELA,y),1)
        for x in range(0,LARGURA_TELA,60): pygame.draw.line(s,(50,40,30),(x,0),(x,ALTURA_TELA),1)
        pygame.draw.rect(s,(40,30,20),(0,CHAO_Y,LARGURA_TELA,ALTURA_TELA-CHAO_Y)); return s

def _fundo_floresta():
    rng=random.Random(12345); s=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); s.fill((20,45,25))
    for tx in range(0,LARGURA_TELA,85):
        th=rng.randint(140,260)
        pygame.draw.rect(s,(50,28,10),(tx+35,CHAO_Y-th,16,th))
        pygame.draw.polygon(s,(25,80,30),[(tx+43,CHAO_Y-th-50),(tx,CHAO_Y-th+40),(tx+85,CHAO_Y-th+40)])
    pygame.draw.rect(s,(35,70,25),(0,CHAO_Y,LARGURA_TELA,ALTURA_TELA-CHAO_Y))
    for gx in range(10,LARGURA_TELA,30):
        gh=rng.randint(6,14)
        pygame.draw.line(s,(50,120,40),(gx,CHAO_Y),(gx-4,CHAO_Y-gh),2)
        pygame.draw.line(s,(50,120,40),(gx,CHAO_Y),(gx+4,CHAO_Y-gh),2)
    return s

def _fundo_castelo():
    s=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); s.fill((60,70,90))
    for bx in range(0,LARGURA_TELA,50): pygame.draw.rect(s,(70,75,85),(bx,40,30,80))
    pygame.draw.rect(s,(75,80,90),(0,120,LARGURA_TELA,CHAO_Y-120))
    for row in range(4):
        for col in range(10):
            off=30 if row%2 else 0
            pygame.draw.rect(s,(65,70,80),(col*80+off,125+row*60,76,56),1)
    pygame.draw.arc(s,(50,55,65),(330,280,140,120),0,math.pi,4)
    pygame.draw.rect(s,(85,85,90),(0,CHAO_Y,LARGURA_TELA,ALTURA_TELA-CHAO_Y)); return s

def _fundo_vulcao():
    s=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); rng=random.Random(99)
    for y in range(ALTURA_TELA):
        t=y/ALTURA_TELA; pygame.draw.line(s,(int(60+40*t),int(10+20*t),5),(0,y),(LARGURA_TELA,y))
    pygame.draw.rect(s,(200,80,10),(0,CHAO_Y,LARGURA_TELA,ALTURA_TELA-CHAO_Y))
    for lx in range(60,LARGURA_TELA,160): pygame.draw.ellipse(s,(255,120,0),(lx,CHAO_Y,80,20))
    for _ in range(15):
        rx,ry=rng.randint(0,LARGURA_TELA-50),rng.randint(CHAO_Y//2,CHAO_Y-10)
        pygame.draw.polygon(s,(60,40,30),[(rx,ry),(rx+rng.randint(20,50),ry),(rx+rng.randint(10,40),ry-rng.randint(20,50))])
    return s

def _fundo_ceu():
    s=pygame.Surface((LARGURA_TELA,ALTURA_TELA)); rng=random.Random(777)
    for y in range(ALTURA_TELA):
        t=y/ALTURA_TELA; pygame.draw.line(s,(int(80+120*t),int(120+100*t),min(255,int(200+40*t))),(0,y),(LARGURA_TELA,y))
    for _ in range(8):
        cx,cy=rng.randint(50,LARGURA_TELA-50),rng.randint(30,200)
        for dx in range(-30,31,15): pygame.draw.circle(s,(240,245,255),(cx+dx,cy),rng.randint(18,30))
    for px in range(0,LARGURA_TELA,200):
        pygame.draw.rect(s,(180,170,160),(px,CHAO_Y,160,40))
        pygame.draw.rect(s,(160,150,140),(px,CHAO_Y,160,10))
    pygame.draw.rect(s,(200,205,215),(0,CHAO_Y,LARGURA_TELA,ALTURA_TELA-CHAO_Y)); return s

def _fundo_final():
    try:
        raw = pygame.image.load("fundofinal.png")
        s = pygame.transform.scale(raw, (LARGURA_TELA, ALTURA_TELA))
        result = pygame.Surface((LARGURA_TELA, ALTURA_TELA)); result.fill((0,0,0))
        result.blit(s,(0,0)); return result.convert()
    except:
        s = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
        for y in range(ALTURA_TELA):
            t = y/ALTURA_TELA
            pygame.draw.line(s,(int(15+15*t),int(5*t),int(20+25*t)),(0,y),(LARGURA_TELA,y))
        pygame.draw.rect(s,(35,5,50),(0,CHAO_Y,LARGURA_TELA,ALTURA_TELA-CHAO_Y)); return s

BG_W = 1100  # fundo mais largo que a tela para permitir scroll de parallax
def _widen(s): return pygame.transform.scale(s,(BG_W,ALTURA_TELA))
def _load_bg(path, fb):
    try: img=pygame.image.load(path).convert(); return pygame.transform.scale(img,(BG_W,ALTURA_TELA))
    except: return _widen(fb())
FUNDOS = [_widen(_fundo_dungeon()), _load_bg("fundofloresta.png",_fundo_floresta), _load_bg("fundocastelo.png",_fundo_castelo), _load_bg("fundovulcão.png",_fundo_vulcao), _load_bg("fundocéu.png",_fundo_ceu), _widen(_fundo_final())]
MUSICAS = [["musica_dungeon.mp3","musica_fundo.mp3"],["musica_floresta.mp3","musica_fundo.mp3"],
           ["musica_castelo.mp3","musica_fundo.mp3"],["musica_vulcao.mp3","musica_fundo.mp3"],
           ["musica_ceu.mp3","musica_fundo.mp3"],["musica_final.mp3","musica_fundo.mp3"]]
MUSICA_BOSS = ["musica_boss.mp3","musica_fundo.mp3"]

_musica_atual = None
def tocar_cenario(idx, boss=False):
    global _musica_atual
    lista = MUSICA_BOSS if boss else MUSICAS[idx]
    for c in lista:
        try: pygame.mixer.music.load(c); pygame.mixer.music.play(-1); _musica_atual=c; return
        except: pass

# ═══════════════════════════════════════════════════════════════
#  DADOS
# ═══════════════════════════════════════════════════════════════
DADOS_INI = [
    # tipos 1-12: vida x2
    (3,6,40,5),(5,8,60,10),(4,7,50,7),(6,9,70,12),(3,5,80,8),(7,10,30,3),
    (2,4,100,15),(5,7,40,6),(4,6,60,9),(6,8,50,7),(3,5,70,10),(8,10,20,2),
    # tipos 13-22
    (2,4,75,8),(4,5,90,10),(3,5,54,5),(4,7,66,6),(3,6,20,8),
    (1,3,80,18),(2,4,28,4),(6,9,15,7),(3,6,35,9),(3,5,30,8),
    # tipos 23-32: tier 3
    (4,7,120,15),(5,9,140,18),(3,6,110,16),(6,9,160,20),(4,7,150,17),
    (7,10,90,12),(3,5,180,22),(5,8,130,16),(4,7,155,19),(6,9,145,18),
    # tipos 33-42: tier 4
    (4,8,200,24),(6,9,220,28),(5,8,195,26),(7,10,250,30),(4,6,230,27),
    (8,11,115,14),(3,5,265,36),(6,8,175,21),(5,7,210,25),(7,9,190,23),
    # tipos 43-52: tier 5
    (5,8,300,34),(7,10,330,38),(6,9,285,32),(8,11,360,42),(5,7,340,36),
    (9,12,140,16),(4,6,380,48),(7,9,250,28),(6,8,315,35),(8,10,280,31),
    # tipos 53-63: tier 6
    (6,9,420,46),(8,11,460,52),(7,10,440,49),(9,12,490,55),(6,8,450,50),
    (10,13,160,18),(5,7,510,60),(8,10,380,42),(7,9,470,52),(9,11,430,47),
    (6,9,530,58),
]
_COMP_EXTRA = ['atirador','carregador','berseker','fantasma','assassino',
               'gigante','curandeiro','bloqueador','morto_vivo','dividido']
COMPORT = {13:'atirador',14:'carregador',15:'dividido',16:'fantasma',17:'berseker',
           18:'gigante',19:'curandeiro',20:'assassino',21:'bloqueador',22:'morto_vivo'}
COMPORT.update({23+i: _COMP_EXTRA[i % len(_COMP_EXTRA)] for i in range(41)})

DADOS_CHAR = [
    {"nome":"Guerreiro",    "sub":"Equilibrado",       "vida":100,"vel":5,"dano":10,"esp":30,"alc":70, "dcd":40,"cor":DOURO},
    {"nome":"Mago",         "sub":"Alto dano/low HP",  "vida":70, "vel":4,"dano":20,"esp":60,"alc":130,"dcd":50,"cor":AZUL},
    {"nome":"Ladino",       "sub":"Rápido e ágil",     "vida":80, "vel":8,"dano":8, "esp":20,"alc":55, "dcd":25,"cor":CINZA},
    {"nome":"Velho Barbudo","sub":"Ancião das runas",  "vida":75, "vel":3,"dano":28,"esp":70,"alc":145,"dcd":55,"cor":BRANCO},
]
DADOS_BOSS = [
    {"nome":"Dragão",           "vida":800, "dano":20,"vel":3,"pat":"fogo"},
    {"nome":"Cavaleiro Sombrio","vida":1000,"dano":25,"vel":4,"pat":"carga"},
    {"nome":"Mago Maligno",     "vida":700, "dano":18,"vel":3,"pat":"magico"},
    {"nome":"Lorde Demônio",    "vida":1200,"dano":30,"vel":5,"pat":"caos"},
    {"nome":"Deus do Caos",     "vida":1600,"dano":40,"vel":6,"pat":"ultimate"},
]
DADOS_FBOSS = [
    {"nome":"Hydra das Trevas",     "vida":1200,"dano":22,"vel":3,"pat":"fogo"},
    {"nome":"Senhor da Escuridão",  "vida":1400,"dano":28,"vel":4,"pat":"carga"},
    {"nome":"Arauto do Caos",       "vida":1600,"dano":25,"vel":3,"pat":"magico"},
    {"nome":"Protetor Amaldiçoado", "vida":1800,"dano":32,"vel":4,"pat":"caos"},
    {"nome":"O INIMIGO FINAL",      "vida":4800,"dano":40,"vel":5,"pat":"ultimate"},
]
# vida dobra a cada fase: 4800*2, *4, *8, *16, *32
DADOS_BOSSFINAL_EXTRA = [
    {"nome":"A SOMBRA ETERNA",   "vida":9600,  "dano":50,"vel":4,"pat":"fogo"},
    {"nome":"O DEVORADOR",       "vida":19200, "dano":60,"vel":5,"pat":"carga"},
    {"nome":"SENHOR DO ABISMO",  "vida":38400, "dano":70,"vel":5,"pat":"magico"},
    {"nome":"O DESTRUIDOR",      "vida":76800, "dano":80,"vel":6,"pat":"caos"},
    {"nome":"A ENTIDADE FINAL",  "vida":153600,"dano":95,"vel":6,"pat":"ultimate"},
]

# ═══════════════════════════════════════════════════════════════
#  ESTADO GLOBAL (efeitos de tela)
# ═══════════════════════════════════════════════════════════════
shake_f = 0; flash_a = 0; flash_c = VERM
personagem = None; inimigos_g = None; projeteis_g = None

# ═══════════════════════════════════════════════════════════════
#  TEXTO FLUTUANTE
# ═══════════════════════════════════════════════════════════════
class TF:
    def __init__(self,x,y,txt,cor=BRANCO,sz=28):
        self.x=float(x); self.y=float(y); self.txt=txt; self.cor=cor
        self.a=255; self.vx=random.uniform(-.5,.5); self.f=pygame.font.Font(None,sz); self.vivo=True
    def update(self):
        self.y-=1.2; self.x+=self.vx; self.a-=5
        if self.a<=0: self.vivo=False
    def draw(self,s):
        if not self.vivo: return
        r=self.f.render(self.txt,True,self.cor); r.set_alpha(max(0,self.a))
        s.blit(r,(int(self.x-r.get_width()//2),int(self.y)))

tfs=[]
def add_tf(x,y,txt,cor=BRANCO,sz=28): tfs.append(TF(x,y,txt,cor,sz))

# ═══════════════════════════════════════════════════════════════
#  PARTÍCULAS
# ═══════════════════════════════════════════════════════════════
class Part:
    def __init__(self,x,y,cor):
        self.x=float(x); self.y=float(y); a=random.uniform(0,2*math.pi); spd=random.uniform(2,7)
        self.vx=math.cos(a)*spd; self.vy=math.sin(a)*spd-3
        self.r=random.randint(3,7); self.cor=cor; self.a=255; self.vivo=True
        r0=self.r; self._surf=_ns(r0*2+4,r0*2+4)   # pre-alocado uma vez
    def update(self):
        self.x+=self.vx; self.y+=self.vy; self.vy+=.4; self.a-=15; self.r=max(1,self.r-.15)
        if self.a<=0: self.vivo=False
    def draw(self,s):
        if not self.vivo: return
        r=int(self.r)
        self._surf.fill((0,0,0,0))
        pygame.draw.circle(self._surf,self.cor+(max(0,int(self.a)),),(r,r),r)
        s.blit(self._surf,(int(self.x-r),int(self.y-r)))

parts=[]
def add_parts(x,y,cor,n=6):
    if len(parts)<400:
        for _ in range(n): parts.append(Part(x,y,cor))

# ═══════════════════════════════════════════════════════════════
#  PROJÉTIL
# ═══════════════════════════════════════════════════════════════
class Proj(pygame.sprite.Sprite):
    def __init__(self,x,y,dir,dano,cor=LARAN):
        super().__init__()
        self.image=_ns(14,8); pygame.draw.ellipse(self.image,cor,(0,0,14,8))
        self.rect=self.image.get_rect(centery=y,centerx=x)
        self.vx=7*dir; self.dano=dano
    def update(self):
        self.rect.x+=self.vx
        if self.rect.right<0 or self.rect.left>LARGURA_TELA: self.kill()

# ═══════════════════════════════════════════════════════════════
#  PROJÉTIL ESPECIAL DO BOSS
# ═══════════════════════════════════════════════════════════════
class BossProj(pygame.sprite.Sprite):
    """Projétil animado com elemento visual — sai do boss em direção ao jogador."""
    _EL={
        'fogo':    {'r':15,'spd':7, 'pcor':(255,100,0)},
        'raio':    {'r':11,'spd':11,'pcor':(180,180,255)},
        'gelo':    {'r':13,'spd':6, 'pcor':(150,230,255)},
        'agua':    {'r':13,'spd':6, 'pcor':(50,160,255)},
        'pedra':   {'r':17,'spd':5, 'pcor':(140,110,70)},
        'ultimate':{'r':19,'spd':8, 'pcor':(255,80,255)},
    }
    def __init__(self,x,y,ax,ay,elem,dano):
        super().__init__()
        self.elem=elem; self.dano=dano; self.t=0
        ed=self._EL.get(elem,self._EL['fogo'])
        self.r=ed['r']; self.pcor=ed['pcor']
        sz=(self.r+8)*2
        self.image=_ns(sz,sz)
        self.rect=self.image.get_rect(center=(x,y))
        self.fx=float(x); self.fy=float(y)
        dx=ax-x; dy=ay-y; dist=max(1,math.sqrt(dx*dx+dy*dy))
        spd=ed['spd']
        self.vx=dx/dist*spd; self.vy=dy/dist*spd
        self._render()

    def update(self):
        self.t+=1
        self.fx+=self.vx; self.fy+=self.vy
        self.rect.center=(int(self.fx),int(self.fy))
        if(self.rect.right<-30 or self.rect.left>LARGURA_TELA+30
                or self.rect.bottom<-30 or self.rect.top>ALTURA_TELA+30):
            self.kill(); return
        if self.t%3==0: add_parts(int(self.fx),int(self.fy),self.pcor,2)
        self._render()

    def _render(self):
        self.image.fill((0,0,0,0))
        r=self.r; sz=self.image.get_width(); cx=cy=sz//2; t=self.t; e=self.elem
        if e=='fogo':
            p=int(abs(math.sin(t*.25))*5)
            pygame.draw.circle(self.image,(255,80,0,50),(cx,cy),r+6+p)
            pygame.draw.circle(self.image,(255,110,0,120),(cx,cy),r+2+p)
            pygame.draw.circle(self.image,(255,80,0,210),(cx,cy),r)
            pygame.draw.circle(self.image,(255,200,0,255),(cx,cy),r//2)
            pygame.draw.circle(self.image,(255,255,180,255),(cx,cy),max(2,r//4))
        elif e=='raio':
            pygame.draw.circle(self.image,(70,70,200),(cx,cy),r)
            pygame.draw.circle(self.image,(150,150,255),(cx,cy),r//2)
            for i in range(6):
                a=math.radians(i*60+t*14)
                x1=cx+int(math.cos(a)*(r//2)); y1=cy+int(math.sin(a)*(r//2))
                ma=a+math.radians(20)
                mx=cx+int(math.cos(ma)*(r-2)); my=cy+int(math.sin(ma)*(r-2))
                x2=cx+int(math.cos(a)*(r+5)); y2=cy+int(math.sin(a)*(r+5))
                pygame.draw.line(self.image,(190,190,255),(x1,y1),(mx,my),2)
                pygame.draw.line(self.image,(220,220,255),(mx,my),(x2,y2),2)
            pygame.draw.circle(self.image,(240,240,255),(cx,cy),4)
        elif e=='gelo':
            pygame.draw.circle(self.image,(55,175,225),(cx,cy),r)
            pygame.draw.circle(self.image,(175,230,255),(cx,cy),r//2)
            for i in range(6):
                a=math.radians(i*60+t*4)
                x2=cx+int(math.cos(a)*(r+5)); y2=cy+int(math.sin(a)*(r+5))
                pygame.draw.line(self.image,(210,245,255),(cx,cy),(x2,y2),2)
                xa=cx+int(math.cos(a+.45)*(r-2)); ya=cy+int(math.sin(a+.45)*(r-2))
                pygame.draw.line(self.image,(190,235,255),(cx,cy),(xa,ya),1)
            pygame.draw.circle(self.image,(235,255,255),(cx,cy),max(2,r//4))
        elif e=='agua':
            p=int(abs(math.sin(t*.13))*4)
            pygame.draw.circle(self.image,(0,85,200),(cx,cy),r)
            for ring in [r//2+p, r//3+1]:
                pygame.draw.circle(self.image,(70,175,255),(cx,cy),ring,3)
            pygame.draw.circle(self.image,(175,220,255),(cx,cy),max(2,r//4))
        elif e=='pedra':
            pygame.draw.circle(self.image,(95,75,50),(cx,cy),r)
            pygame.draw.circle(self.image,(150,125,85),(cx-3,cy-3),r//3)
            for i in range(4):
                a=math.radians(i*90+15)
                x2=cx+int(math.cos(a)*r); y2=cy+int(math.sin(a)*r)
                pygame.draw.line(self.image,(55,40,25),(cx,cy),(x2,y2),3)
            pygame.draw.circle(self.image,(175,150,105),(cx,cy),max(2,r//5))
        else:  # ultimate — anel de todos os elementos girando
            UCORS=[(255,60,0),(180,180,255),(80,220,255),(50,175,255),(100,80,55),(255,0,210)]
            for i,uc in enumerate(UCORS):
                a=math.radians(i*60+t*11)
                px=cx+int(math.cos(a)*(r-4)); py=cy+int(math.sin(a)*(r-4))
                pygame.draw.circle(self.image,uc,(px,py),7)
            pygame.draw.circle(self.image,(255,255,255),(cx,cy),r//3)
            pygame.draw.circle(self.image,(200,200,255),(cx,cy),max(2,r//6))

# ═══════════════════════════════════════════════════════════════
#  PERSONAGEM
# ═══════════════════════════════════════════════════════════════
class Personagem(pygame.sprite.Sprite):
    def __init__(self,ti):
        super().__init__()
        d=DADOS_CHAR[ti]; self.ti=ti; self.image=imgs_char[ti]
        self._goff=off_char[ti]   # pixels transparentes embaixo do sprite
        self.rect=self.image.get_rect(); self.rect.midbottom=(LARGURA_TELA//2, CHAO_Y+self._goff)
        self.VMAX=d["vida"]; self.vel=d["vel"]; self.DATQ=d["dano"]
        self.DESP=d["esp"]; self.ALC=d["alc"]; self.DCD=d["dcd"]
        self.vida=self.VMAX; self.dir=True
        self.mp=100; self.VMAX_MP=100
        self.bloq=False; self.bloq_flash=0
        self.vy=0.0; self.chao=True
        self.fatq=0; self.esp_ativo=False; self.ang=0
        self.chain=0; self.chain_t=0; self.chain_cd=0
        self.inv=0; self.combo=0; self.fcombo=0

    def update(self):
        global shake_f, flash_a, flash_c
        k=pygame.key.get_pressed()
        if k[pygame.K_LEFT]:
            self.rect.x=max(0, self.rect.x-self.vel); self.dir=False
        if k[pygame.K_RIGHT]:
            self.rect.x=min(LARGURA_TELA-self.rect.width, self.rect.x+self.vel); self.dir=True
        if k[pygame.K_UP] and self.chao:
            self.vy=-15.0; self.chao=False; _play(som_pulo)
        self.vy+=.8; self.rect.y+=int(self.vy)
        solo=CHAO_Y+self._goff
        if self.rect.bottom>=solo: self.rect.bottom=solo; self.vy=0.0; self.chao=True
        if self.fatq>0:
            self.fatq-=1; self.ang=(self.ang+(30 if self.esp_ativo else 20))%360
            if self.fatq==0: self.esp_ativo=False
        if self.chain_t>0: self.chain_t-=1
        else: self.chain=0
        if self.chain_cd>0: self.chain_cd-=1
        if self.fcombo>0: self.fcombo-=1
        else: self.combo=0
        if self.inv>0: self.inv-=1
        self.bloq=bool(k[pygame.K_LALT])
        if self.bloq_flash>0: self.bloq_flash-=1

    def _alc(self,esp=False):
        m=self.ALC*(2 if esp else 1); return self.rect.inflate(m*2,0)

    def _dano_chain(self):
        if self.chain==2: return int(self.DATQ*1.2)
        if self.chain>=3: return int(self.DATQ*2.0)
        return self.DATQ

    def iniciar_atq(self,esp=False):
        self.fatq=50 if esp else 15; self.esp_ativo=esp
        if not esp and self.chain_cd==0:
            self.chain = self.chain+1 if self.chain_t>0 else 1
            self.chain_t=30
            if self.chain>=3: self.chain_cd=30; self.chain=0

    def atacar(self,alvo):
        if not self._alc().colliderect(alvo.rect): return False,0
        d=self._dano_chain(); alvo.hit(d,self); _play(som_atq)
        self.combo+=1; self.fcombo=90
        add_parts(alvo.rect.centerx,alvo.rect.centery,LARAN)
        return True,d

    def atacar_esp(self,alvo):
        if not self._alc(True).colliderect(alvo.rect): return False,0
        d=self.DESP; alvo.hit(d,self); _play(som_atq)
        self.combo+=1; self.fcombo=90
        add_parts(alvo.rect.centerx,alvo.rect.centery,CIANO,10)
        return True,d

    def dano(self,d):
        global shake_f, flash_a, flash_c
        if self.inv>0: return False
        if self.bloq:
            d=max(1,d//3); self.inv=18; self.bloq_flash=16
            self.vida=max(0,self.vida-d)
            shake_f=3; flash_a=60; flash_c=(200,220,255)
            add_parts(self.rect.centerx,self.rect.top-10,(255,240,120),8)
            _play(som_col); return True
        self.vida=max(0,self.vida-d); self.inv=60
        shake_f=8; flash_a=120; flash_c=VERM; _play(som_col); return True

    def curar(self,q): self.vida=min(self.VMAX,self.vida+q)

    def desenhar(self,s):
        img=self.image if self.dir else pygame.transform.flip(self.image,True,False)
        if not(self.inv>0 and (self.inv//5)%2==0):
            s.blit(img,self.rect.topleft)
        if self.fatq>0:
            cx=self.rect.centerx; cy=self.rect.centery-20
            if self.esp_ativo:
                R=72  # raio da órbita
                if self.ti==0:  # Guerreiro — 5 machados girando em órbita circular
                    for i in range(5):
                        a=math.radians(self.ang*4+i*72)
                        ox=int(math.cos(a)*R); oy=int(math.sin(a)*R)
                        # arma aponta tangencialmente (perpendicular ao raio) — aparência de girar
                        mr=pygame.transform.rotozoom(machado,-(self.ang*4+i*72)+90,1.5)
                        r=mr.get_rect(center=(cx+ox,cy+oy))
                        s.blit(mr,r.topleft)
                elif self.ti==1:  # Mago — 6 chamas azuis girando em órbita circular
                    for i in range(6):
                        a=math.radians(self.ang*4+i*60)
                        ox=int(math.cos(a)*R); oy=int(math.sin(a)*R)
                        fcx=cx+ox; fcy=cy+oy
                        pulse=int(abs(math.sin((self.ang+i*30)*0.15))*8)
                        for gr,ga,gcor in [(18+pulse,70,(80,80,255)),(12+pulse,140,CIANO),(7+pulse,220,(220,245,255))]:
                            gs=_ns(gr*2+2,gr*2+2)
                            pygame.draw.circle(gs,gcor+(ga,),(gr,gr),gr)
                            s.blit(gs,(fcx-gr,fcy-gr))
                elif self.ti==2:  # Ladino — 5 espadas girando em órbita circular
                    for i in range(5):
                        a=math.radians(self.ang*4+i*72)
                        ox=int(math.cos(a)*R); oy=int(math.sin(a)*R)
                        me=pygame.transform.rotozoom(espada_img,-(self.ang*4+i*72)+90,1.4)
                        r=me.get_rect(center=(cx+ox,cy+oy))
                        s.blit(me,r.topleft)
                else:  # Velho Barbudo — 3 machadobarba girando em órbita
                    for i in range(3):
                        a=math.radians(self.ang*3+i*120)
                        ox=int(math.cos(a)*R); oy=int(math.sin(a)*R)
                        mr=pygame.transform.rotozoom(machadobarba,-(self.ang*3+i*120)+90,1.5)
                        r=mr.get_rect(center=(cx+ox,cy+oy))
                        s.blit(mr,r.topleft)
            else:
                lado=1 if self.dir else -1
                if self.ti==0:  # Guerreiro — machado giratório
                    mr=pygame.transform.rotozoom(machado,self.ang,1.8)
                    r=mr.get_rect(center=self.rect.center)
                    r.x+=65*lado
                    s.blit(mr,r.topleft)
                elif self.ti==1:  # Mago — cajado inclinado + orbe mágico
                    ang_caj=-55*lado
                    mc=pygame.transform.rotozoom(cajado_img,ang_caj,1.8)
                    r=mc.get_rect(center=self.rect.center)
                    r.x+=55*lado; r.y-=12
                    s.blit(mc,r.topleft)
                    pulse=int(abs(math.sin(self.ang*0.12))*7)
                    gx=self.rect.centerx+80*lado; gy=self.rect.centery-38
                    for gr,ga,gcor in [(20+pulse,50,AZUL),(14+pulse,110,CIANO),(9+pulse,200,(200,240,255))]:
                        gs=_ns(gr*2+2,gr*2+2)
                        pygame.draw.circle(gs,gcor+(ga,),(gr,gr),gr)
                        s.blit(gs,(gx-gr,gy-gr))
                elif self.ti==2:  # Ladino — espada com slash em arco
                    slash_t=(15-self.fatq)/15
                    ang_esp=int((65-130*slash_t)*lado)
                    me=pygame.transform.rotozoom(espada_img,ang_esp,1.8)
                    r=me.get_rect(center=self.rect.center)
                    r.x+=55*lado; r.y-=8
                    s.blit(me,r.topleft)
                else:  # Velho Barbudo — machadobarba giratório
                    mr=pygame.transform.rotozoom(machadobarba,self.ang,1.8)
                    r=mr.get_rect(center=self.rect.center)
                    r.x+=65*lado
                    s.blit(mr,r.topleft)

        # ── BLOQUEIO ──
        if self.bloq:
            lado=1 if self.dir else -1
            if self.ti==1:   # Mago: cajado ereto, na frente (mesma altura do tronco)
                bx=self.rect.centerx+lado*55; by=self.rect.centery+8
                bimg=pygame.transform.rotozoom(cajado_img,8*lado,3.2)
            elif self.ti==0:  # Guerreiro: machado horizontal de defesa
                bx=self.rect.centerx+lado*58; by=self.rect.centery-10
                bimg=pygame.transform.rotozoom(machado,55*lado,3.2)
            elif self.ti==2:   # Ladino: espada diagonal de defesa
                bx=self.rect.centerx+lado*56; by=self.rect.centery-12
                bimg=pygame.transform.rotozoom(espada_img,50*lado,3.2)
            else:              # Velho Barbudo: machadobarba horizontal de defesa
                bx=self.rect.centerx+lado*58; by=self.rect.centery-10
                bimg=pygame.transform.rotozoom(machadobarba,55*lado,3.2)
            if not self.dir: bimg=pygame.transform.flip(bimg,True,False)
            br=bimg.get_rect(center=(bx,by)); s.blit(bimg,br.topleft)
            # brilho pulsante ao redor da arma
            pulse=int(abs(math.sin(pygame.time.get_ticks()*.007))*14)+18
            gs=_ns(pulse*2+2,pulse*2+2)
            pygame.draw.circle(gs,(180,220,255,75),(pulse,pulse),pulse)
            s.blit(gs,(bx-pulse,by-pulse))
            # impacto do golpe — maior e mais vistoso
            if self.bloq_flash>0:
                pct=self.bloq_flash/16
                rf=int(40+pct*34)
                gf=_ns(rf*2+2,rf*2+2); al=int(pct*240)
                pygame.draw.circle(gf,(255,240,80,al),(rf,rf),rf)
                pygame.draw.circle(gf,(255,255,200,min(255,al+60)),(rf,rf),rf*2//3)
                pygame.draw.circle(gf,(255,255,255,min(255,al+120)),(rf,rf),rf//3)
                s.blit(gf,(bx-rf,by-rf))
                for i in range(10):
                    a=math.radians(i*36+self.bloq_flash*22)
                    ln=int(pct*32+10)
                    pygame.draw.line(s,(255,230,50),
                        (bx+int(math.cos(a)*14),by+int(math.sin(a)*14)),
                        (bx+int(math.cos(a)*(14+ln)),by+int(math.sin(a)*(14+ln))),3)

# ═══════════════════════════════════════════════════════════════
#  INIMIGO
# ═══════════════════════════════════════════════════════════════
class Inimigo(pygame.sprite.Sprite):
    CD=90
    def __init__(self,tipo,dif=1.0):
        super().__init__()
        self.tipo=tipo; idx=tipo-1
        vm,vx,vb,db=DADOS_INI[idx]; self.image=imgs_ini[idx]; self.rect=self.image.get_rect()
        self.gif=_gif_map.get(idx)  # GifAnim se for inimigo animado, None caso contrário
        bv=int((dif-1)*2)
        self.vel=random.randint(vm+bv,vx+bv); self.vida=int(vb*dif)
        self.vmax=self.vida; self.dano=max(1,int(db*dif))
        goff=off_ini[idx]   # alinha o sprite ao chão real
        if random.random()<.5: self.rect.midbottom=(LARGURA_TELA+60,CHAO_Y+goff); self.dir=False
        else: self.rect.midbottom=(-60,CHAO_Y+goff); self.dir=True
        self.kb=0.0; self.tatq=self.CD//2; self.fatq=0; self.flash=0
        self.comp=COMPORT.get(tipo,'normal'); self._init_comp()

    def _init_comp(self):
        c=self.comp
        if c=='atirador': self.tproj=120; self.dmin=180
        elif c=='carregador': self.carg=False; self.tcarg=0
        elif c=='dividido': self.divided=False
        elif c=='fantasma': self.tfant=0; self.inv_fant=False
        elif c=='berseker': self.berk=False
        elif c=='curandeiro': self.tcura=60
        elif c=='assassino': self.ttele=180
        elif c=='morto_vivo': self.revived=False
        elif c=='gigante': self.tpisada=80; self.CD=120  # ataque mais lento mas pesado

    def hit(self,d,atk=None):
        if self.comp=='bloqueador' and atk:
            front=(self.dir and atk.rect.centerx<self.rect.centerx) or \
                  (not self.dir and atk.rect.centerx>self.rect.centerx)
            if front: d=d//2
        if self.comp=='fantasma' and self.inv_fant:
            add_tf(self.rect.centerx,self.rect.top-20,"IMUNE!",CIANO); return
        self.vida-=d; self.flash=4
        dr=1 if(atk and atk.rect.centerx<self.rect.centerx)else -1; self.kb=float(dr*12)

    def update(self):
        global inimigos_g, projeteis_g
        if self.gif: self.gif.tick(); self.image=self.gif.current()
        if abs(self.kb)>.5: self.rect.x+=int(self.kb); self.kb*=.65
        else:
            self.kb=0.0; self._mover()
        self.rect.x=max(-self.rect.width,min(LARGURA_TELA,self.rect.x))
        if self.tatq>0: self.tatq-=1
        if self.fatq>0: self.fatq-=1
        if self.flash>0: self.flash-=1
        if personagem and self.rect.inflate(30,0).colliderect(personagem.rect):
            if self.tatq<=0:
                personagem.dano(self.dano); self.tatq=self.CD; self.fatq=18
        c=self.comp
        if c=='atirador': self._atirador()
        elif c=='carregador': self._carregador()
        elif c=='fantasma': self._fantasma()
        elif c=='berseker': self._berseker()
        elif c=='curandeiro': self._curandeiro()
        elif c=='assassino': self._assassino()
        elif c=='gigante': self._gigante()

    def _mover(self):
        if not personagem: return
        dx=personagem.rect.centerx-self.rect.centerx
        stop=self.rect.width//2+personagem.rect.width//2+8
        if self.comp=='atirador':
            if abs(dx)<self.dmin: self.rect.x-=self.vel if dx>0 else -self.vel
            elif abs(dx)>self.dmin+60: self.rect.x+=self.vel if dx>0 else -self.vel
        elif self.comp=='carregador' and self.carg:
            self.rect.x+=18 if dx>0 else -18
            if abs(dx)<stop or abs(dx)>400: self.carg=False; self.tcarg=120
        else:
            if abs(dx)>stop: self.rect.x+=self.vel if dx>0 else -self.vel
        if abs(dx)>stop: self.dir=dx>0

    def _atirador(self):
        if not(projeteis_g and personagem): return
        self.tproj-=1
        if self.tproj<=0:
            self.tproj=120; dx=personagem.rect.centerx-self.rect.centerx
            projeteis_g.add(Proj(self.rect.centerx,self.rect.centery,1 if dx>0 else -1,self.dano))
    def _carregador(self):
        if self.tcarg>0: self.tcarg-=1; return
        if personagem:
            dx=abs(personagem.rect.centerx-self.rect.centerx)
            if dx<300 and dx>60 and not self.carg: self.carg=True
    def _fantasma(self):
        self.tfant+=1
        if self.tfant==120: self.inv_fant=True
        if self.tfant>=180: self.inv_fant=False; self.tfant=0
    def _berseker(self):
        low=self.vida<self.vmax*.33
        if low and not self.berk: self.berk=True; self.vel=min(12,self.vel+4)
        elif not low and self.berk: self.berk=False; self.vel=max(1,self.vel-4)
    def _curandeiro(self):
        if not inimigos_g: return
        self.tcura-=1
        if self.tcura<=0:
            self.tcura=60
            for e in inimigos_g:
                if e is not self and abs(e.rect.centerx-self.rect.centerx)<120:
                    e.vida=min(e.vmax,e.vida+3)
    def _assassino(self):
        if not personagem: return
        self.ttele-=1
        if self.ttele<=0:
            self.ttele=180; off=random.choice([-80,80])
            self.rect.centerx=max(0,min(LARGURA_TELA,personagem.rect.centerx+off))
            add_parts(self.rect.centerx,self.rect.centery,ROXO,8)

    def _gigante(self):
        """Pisada pesada: vibra o chão periodicamente e empurra o jogador ao atacar."""
        global shake_f, flash_a, flash_c
        self.tpisada-=1
        if self.tpisada<=0:
            self.tpisada=80; shake_f=max(shake_f,5)
            add_parts(self.rect.centerx,self.rect.bottom,MARROM,8)
        # Ao colidir, aplica knockback extra no jogador
        if personagem and self.fatq>14:
            dx=1 if personagem.rect.centerx>self.rect.centerx else -1
            personagem.rect.x=max(0,min(LARGURA_TELA-personagem.rect.width,
                                         personagem.rect.x+dx*18))

    def draw_hp(self,s):
        w=max(40,self.rect.width); h=6; x,y=self.rect.left,self.rect.top-12
        p=max(0.0,self.vida/self.vmax)
        cor=VERDE if p>.5 else(AMAR if p>.25 else VERM)
        pygame.draw.rect(s,(60,0,0),(x,y,w,h))
        pygame.draw.rect(s,cor,(x,y,int(w*p),h))
        pygame.draw.rect(s,PRETO,(x,y,w,h),1)

# ═══════════════════════════════════════════════════════════════
#  BOSS
# ═══════════════════════════════════════════════════════════════
# Mapeamento padrão: padrão de ataque → elemento visual do especial
_PAT_ELEM       = {'fogo':'fogo','carga':'raio','magico':'gelo','caos':'pedra','ultimate':'ultimate'}
# FinalBosses: Arauto do Caos usa 'agua' em vez de 'gelo'
_PAT_ELEM_FINAL = {'fogo':'fogo','carga':'raio','magico':'agua','caos':'pedra','ultimate':'ultimate'}

class Boss:
    def __init__(self,idx):
        d=DADOS_BOSS[idx]; self.idx=idx; self.nome=d["nome"]
        self.image=imgs_boss[idx]; self.rect=self.image.get_rect()
        self.gif=_gif_boss_map.get(idx)
        self.rect.midbottom=(LARGURA_TELA+80, CHAO_Y+off_boss[idx])
        self.vida=d["vida"]; self.vmax=d["vida"]; self.dano=d["dano"]
        self.vel=d["vel"]; self.pat=d["pat"]; self.dir=False
        self.kb=0.0; self.tatq=90; self.fatq=0; self.flash=0
        self.fase=1; self.tesp=180
        self.elem=_PAT_ELEM.get(self.pat,'fogo')

    def hit(self,d,atk=None):
        self.vida=max(0,self.vida-d); self.flash=4
        dr=1 if(atk and atk.rect.centerx<self.rect.centerx)else -1; self.kb=float(dr*8)

    def update(self):
        if self.gif: self.gif.tick(); self.image=self.gif.current()
        prop=self.vida/self.vmax
        self.fase=3 if prop<.30 else(2 if prop<.60 else 1)
        v=self.vel+(self.fase-1)
        if abs(self.kb)>.5: self.rect.x+=int(self.kb); self.kb*=.65
        else:
            self.kb=0.0
            if personagem:
                dx=personagem.rect.centerx-self.rect.centerx
                stop=self.rect.width//2+personagem.rect.width//2+10
                if abs(dx)>stop: self.rect.x+=v if dx>0 else -v; self.dir=dx>0
        self.rect.x=max(-self.rect.width,min(LARGURA_TELA,self.rect.x))
        if self.tatq>0: self.tatq-=1
        if self.fatq>0: self.fatq-=1
        if self.flash>0: self.flash-=1
        if personagem and self.rect.colliderect(personagem.rect):
            if self.tatq<=0:
                cd=max(40,90-(self.fase-1)*20)
                personagem.dano(self.dano*(self.fase//2+1)//2+self.dano//2)
                self.tatq=cd; self.fatq=20
        self.tesp-=1
        if self.tesp<=0:
            self.tesp=max(90,240-self.fase*50); self._esp()

    def _esp(self):
        if personagem is None: return
        ax=personagem.rect.centerx; ay=personagem.rect.centery
        x=self.rect.centerx; y=self.rect.centery-10
        e=self.elem; f=self.fase; d=int(self.dano*1.6)
        if e=='fogo':
            n=1 if f==1 else(3 if f==2 else 5)
            spr=0 if n==1 else 28
            for i in range(n):
                off=int((i-(n-1)/2)*spr)
                projeteis_g.add(BossProj(x,y,ax+off,ay,e,d))
        elif e=='raio':
            n=3 if f==1 else(5 if f==2 else 7)
            for i in range(n):
                off=int((i-(n-1)/2)*32)
                projeteis_g.add(BossProj(x,y,ax+off,ay,e,d))
        elif e=='gelo':
            n=3 if f==1 else(5 if f==2 else 7)
            for i in range(n):
                off=int((i-(n-1)/2)*30)
                projeteis_g.add(BossProj(x,y,ax+off,ay,e,d))
        elif e=='agua':
            n=2 if f==1 else(4 if f==2 else 6)
            for i in range(n):
                off=int((i-(n-1)/2)*36)
                projeteis_g.add(BossProj(x,y,ax+off,ay,e,d))
        elif e=='pedra':
            n=1 if f==1 else(2 if f==2 else 3)
            for i in range(n):
                off=int((i-(n-1)/2)*42)
                projeteis_g.add(BossProj(x,y,ax+off,ay,e,d))
        else:  # ultimate — um de cada elemento
            elems=['fogo','raio','gelo','agua','pedra']
            for i,el in enumerate(elems):
                off=int((i-2)*32)
                projeteis_g.add(BossProj(x,y,ax+off,ay,el,d))
            if f==3:  # fase final: segunda salva centralizada
                for el in ['raio','gelo']:
                    projeteis_g.add(BossProj(x,y,ax,ay,el,d))

    def draw_hp(self,s):
        w=300; h=18; x=LARGURA_TELA//2-w//2; y=ALTURA_TELA-42
        p=max(0.0,self.vida/self.vmax)
        pygame.draw.rect(s,(60,0,0),(x-1,y-1,w+2,h+2))
        pygame.draw.rect(s,VERM,(x,y,w,h))
        pygame.draw.rect(s,DOURO,(x,y,int(w*p),h))
        t=FI.render(f"BOSS: {self.nome}  {self.vida}/{self.vmax}",True,BRANCO)
        s.blit(t,(x+w//2-t.get_width()//2,y+1))

# ═══════════════════════════════════════════════════════════════
#  BOSS FINAL
# ═══════════════════════════════════════════════════════════════
class FinalBoss(Boss):
    def __init__(self, fi):
        d = DADOS_FBOSS[fi]; self.fi = fi
        self.idx = fi; self.nome = d["nome"]
        self.image = fboss_imgs[fi]; self.rect = self.image.get_rect()
        self.gif = _gif_fboss_map.get(fi)
        self.rect.midbottom = (LARGURA_TELA+80, CHAO_Y+off_fboss[fi])
        self.vida = d["vida"]; self.vmax = d["vida"]; self.dano = d["dano"]
        self.vel = d["vel"]; self.pat = d["pat"]; self.dir = False
        self.kb = 0.0; self.tatq = 90; self.fatq = 0; self.flash = 0
        self.fase = 1; self.tesp = 180
        self.elem = _PAT_ELEM_FINAL.get(self.pat, 'fogo')

class BossFinalExtra(Boss):
    """Cadeia de 5 bosses que aparece após derrotar O INIMIGO FINAL."""
    def __init__(self, fi):
        d = DADOS_BOSSFINAL_EXTRA[fi]; self.fi = fi
        self.idx = fi; self.nome = d["nome"]
        self.image = extra_boss_imgs[fi]; self.rect = self.image.get_rect()
        self.gif = _gif_extra_boss_map.get(fi)
        self.rect.midbottom = (LARGURA_TELA+80, CHAO_Y+off_extra_boss[fi])
        self.vida = d["vida"]; self.vmax = d["vida"]; self.dano = d["dano"]
        self.vel = d["vel"]; self.pat = d["pat"]; self.dir = False
        self.kb = 0.0; self.tatq = 90; self.fatq = 0; self.flash = 0
        self.fase = 1; self.tesp = 180
        self.elem = _PAT_ELEM_FINAL.get(self.pat, 'fogo')

# ═══════════════════════════════════════════════════════════════
#  ITEM
# ═══════════════════════════════════════════════════════════════
class Item(pygame.sprite.Sprite):
    def __init__(self,x,sub='pocao'):
        super().__init__()
        self.sub=sub; self.image=imgs_item.get(sub,imgs_item['pocao'])
        self.rect=self.image.get_rect(); self.rect.x=x
        self.rect.bottom=CHAO_Y + off_item_d.get(sub, 0)
    def aplicar(self,p,ig=None):
        _play(som_colt)
        if self.sub=='pocao': p.curar(25); add_tf(p.rect.centerx,p.rect.top,"+25 HP",VERDE,30)
        elif self.sub=='bota': p.curar(50); add_tf(p.rect.centerx,p.rect.top,"+50 HP",CIANO,30)
        elif self.sub=='bomba':
            if ig:
                for e in list(ig): e.hit(40); add_parts(e.rect.centerx,e.rect.centery,LARAN,12)
            add_tf(p.rect.centerx,p.rect.top,"BOMBA!",LARAN,34); _play(som_bomb)
        elif self.sub=='mp10':
            p.mp=min(p.VMAX_MP,p.mp+10)
            add_tf(p.rect.centerx,p.rect.top,"+10 MP",(100,200,255),28)
        elif self.sub=='mp20':
            p.mp=min(p.VMAX_MP,p.mp+20)
            add_tf(p.rect.centerx,p.rect.top,"+20 MP",(80,140,255),28)
        elif self.sub=='mp50':
            p.mp=min(p.VMAX_MP,p.mp+50)
            add_tf(p.rect.centerx,p.rect.top,"+50 MP",(180,80,255),30)
        elif self.sub=='mpfull':
            p.mp=p.VMAX_MP
            add_tf(p.rect.centerx,p.rect.top,"MP CHEIO!",(255,220,0),34)

def mk_item(x=None,sub=None):
    if x is None: x=random.randint(10,LARGURA_TELA-42)
    if sub is None:
        r=random.random()
        if r<.48:   sub='pocao'
        elif r<.70: sub='bota'
        elif r<.78: sub='bomba'
        elif r<.90: sub='mp10'
        elif r<.97: sub='mp20'
        elif r<.99: sub='mp50'
        else:       sub='mpfull'
    return Item(x,sub)

# ═══════════════════════════════════════════════════════════════
#  RANKING
# ═══════════════════════════════════════════════════════════════
RK_FILE="ranking.json"
def salvar_rk(pts,onda,nome):
    try: data=json.load(open(RK_FILE))
    except: data=[]
    data.append({"pts":pts,"onda":onda,"nome":nome})
    data.sort(key=lambda x:x["pts"],reverse=True); data=data[:5]
    try: json.dump(data,open(RK_FILE,"w"))
    except: pass
    return data

def load_rk():
    try: return json.load(open(RK_FILE))
    except: return []

# ═══════════════════════════════════════════════════════════════
#  UTILITÁRIOS
# ═══════════════════════════════════════════════════════════════
def txt(s,t,f,c,x,y):
    r=f.render(t,True,c); s.blit(r,r.get_rect(center=(x,y)))

def idx_cen(onda):
    if onda<5: return 0
    if onda<10: return 1
    if onda<15: return 2
    if onda<20: return 3
    if onda<21: return 4
    return 5

def hud(p,vidas,pts,onda,boss=None):
    larg,alt=210,22; prop=max(0.0,p.vida/p.VMAX)
    t=pygame.time.get_ticks()
    if prop<=.25: bc=(min(255,220+int(abs(math.sin(t/200))*80)),30,30)
    elif prop<=.5: bc=AMAR
    else: bc=VERDE
    pygame.draw.rect(tela,CINZA,(9,9,larg+2,alt+2))
    pygame.draw.rect(tela,VERM,(10,10,larg,alt))
    pygame.draw.rect(tela,bc,(10,10,int(larg*prop),alt))
    ht=FI.render(f"HP {p.vida}/{p.VMAX}",True,BRANCO)
    tela.blit(ht,(10+larg//2-ht.get_width()//2,12))
    mp_prop=max(0.0,p.mp/p.VMAX_MP)
    mp_cor=(50,120,255) if mp_prop>0.25 else (100,60,180)
    pygame.draw.rect(tela,CINZA,(9,34,larg+2,14))
    pygame.draw.rect(tela,(20,20,80),(10,35,larg,12))
    pygame.draw.rect(tela,mp_cor,(10,35,int(larg*mp_prop),12))
    mt=FI.render(f"MP {p.mp}/{p.VMAX_MP}",True,BRANCO)
    tela.blit(mt,(10+larg//2-mt.get_width()//2,35))
    for i in range(vidas):
        pygame.draw.circle(tela,VERM,(230+i*22,18),7)
        pygame.draw.circle(tela,ROSA,(227+i*22,15),4)
    tela.blit(FP.render(f"Pontuação: {pts}",True,BRANCO),(10,45))
    tela.blit(FP.render(f"Onda: {onda}",True,AMAR),(10,75))
    d=DADOS_CHAR[p.ti]; tela.blit(FI.render(d["nome"],True,d["cor"]),(10,100))
    if p.combo>1 and p.fcombo>0:
        txt(tela,f"COMBO x{p.combo}!",FM,LARAN if p.combo>=5 else AMAR,LARGURA_TELA//2,40)
    for ci in range(p.chain):
        pygame.draw.circle(tela,AMAR if ci<2 else LARAN,(LARGURA_TELA-30-ci*22,25),8)
    if boss: boss.draw_hp(tela)

# ═══════════════════════════════════════════════════════════════
#  TELAS
# ═══════════════════════════════════════════════════════════════
def tela_sel():
    sel=0
    while True:
        tela.blit(FUNDOS[0],(-(BG_W-LARGURA_TELA)//2,0))
        ov=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA); ov.fill((0,0,0,160)); tela.blit(ov,(0,0))
        txt(tela,"FÚRIA DAS MASMORRAS",FP,(180,120,15),LARGURA_TELA//2,30)
        txt(tela,"ESCOLHA SEU PERSONAGEM",FM,AMAR,LARGURA_TELA//2,68)
        cw,sx=160,(LARGURA_TELA-160*4-20*3)//2
        for i,d in enumerate(DADOS_CHAR):
            cx=sx+i*(cw+20); cy=110; sel_e=(i==sel)
            cs=pygame.Surface((cw,300),pygame.SRCALPHA); cs.fill((0,0,0,180)); tela.blit(cs,(cx,cy))
            pygame.draw.rect(tela,d["cor"] if sel_e else CINZA,(cx,cy,cw,300),3 if sel_e else 1)
            img=imgs_char[i]; tela.blit(img,img.get_rect(centerx=cx+cw//2,top=cy+15))
            txt(tela,d["nome"],FP,d["cor"] if sel_e else BRANCO,cx+cw//2,cy+150)
            txt(tela,d["sub"],FI,CINZA,cx+cw//2,cy+174)
            for si,(st,sc) in enumerate([(f"HP:{d['vida']}",VERDE),(f"Vel:{d['vel']}",CIANO),(f"Dano:{d['dano']}",LARAN),(f"Alc:{d['alc']}",AMAR)]):
                txt(tela,st,FI,sc,cx+cw//2,cy+200+si*20)
        txt(tela,"← → Selecionar   ESPAÇO Confirmar   Q Sair",FI,BRANCO,LARGURA_TELA//2,ALTURA_TELA-35)
        pygame.display.flip(); clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_LEFT: sel=(sel-1)%4
                elif ev.key==pygame.K_RIGHT: sel=(sel+1)%4
                elif ev.key==pygame.K_SPACE: return sel
                elif ev.key==pygame.K_q: pygame.quit(); sys.exit()

def _fundo_menu():
    """Fundo de pedra escuro pré-renderizado para o menu."""
    s = pygame.Surface((LARGURA_TELA, ALTURA_TELA))
    # Gradiente escuro do topo para baixo
    for y in range(ALTURA_TELA):
        t = y / ALTURA_TELA
        pygame.draw.line(s, (int(10+18*t), int(5+8*t), int(18+12*t)), (0,y),(LARGURA_TELA,y))
    # Tijolos de pedra
    rng2 = random.Random(1313)
    for row in range(24):
        for col in range(11):
            off = 40 if row%2 else 0
            bx = col*80 + off - 40; by = row*28
            sh = rng2.randint(28,58)
            pygame.draw.rect(s,(sh,sh//3,sh+6),(bx+2,by+2,75,25))
            pygame.draw.rect(s,(max(0,sh-18),sh//5,max(0,sh-8)),(bx+2,by+2,75,25),1)
    # Chão
    pygame.draw.rect(s,(38,22,12),(0,528,LARGURA_TELA,ALTURA_TELA-528))
    rng3 = random.Random(222)
    for fx in range(-50,LARGURA_TELA,100):
        pygame.draw.rect(s,(32,18,9),(fx+2,530,96,26),1)
        pygame.draw.rect(s,(32,18,9),(fx+52,558,96,26),1)
    # Vinheta nas bordas
    vig = pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA)
    for r in range(0,280,14):
        a = min(200,r//2)
        for cx2,cy2 in [(0,0),(LARGURA_TELA,0),(0,ALTURA_TELA),(LARGURA_TELA,ALTURA_TELA)]:
            pygame.draw.circle(vig,(0,0,0,a),(cx2,cy2),r)
    s.blit(vig,(0,0))
    return s

def _tocha(surf, x, y, t):
    """Desenha tocha na parede com chama animada."""
    # Suporte de metal
    pygame.draw.rect(surf,(55,35,10),(x-3,y+5,6,30))
    pygame.draw.rect(surf,(75,50,16),(x-11,y-2,22,9))
    pygame.draw.rect(surf,(60,40,12),(x-7,y-12,14,11))
    pygame.draw.ellipse(surf,(90,55,15),(x-7,y-5,14,8))
    # Chama (animada com sin)
    flk = math.sin(t*0.19)*3 + math.sin(t*0.37)*2
    fx = x + int(flk)
    # camadas: vermelho/laranja/amarelo/branco
    for (dr,dg,db),(pw,ph,poy) in [
        ((170,30,0),(12,28,0)), ((230,90,0),(9,22,6)),
        ((255,175,0),(6,16,11)),((255,240,120),(3,9,16))]:
        pts=[(fx-pw,y+poy-2),(fx+pw,y+poy-2),(fx+pw//2,y+poy-ph),(fx-pw//2,y+poy-ph)]
        pygame.draw.polygon(surf,(dr,dg,db),pts)
    # Reflexo de luz na parede
    gr = int(70+math.sin(t*0.19)*8)
    gs = _ns(gr*2,gr*2)
    pygame.draw.circle(gs,(90,45,8,55),(gr,gr),gr)
    surf.blit(gs,(x-gr,y-gr),special_flags=pygame.BLEND_RGB_ADD)

def menu_ini():
    _bg = _fundo_menu()
    embers = []   # [x, y, vx, vy, vida]
    t = 0

    while True:
        t += 1

        # Spawn brasas das tochas
        if t%4==0:
            for tx in [125, LARGURA_TELA-125]:
                embers.append([float(tx+random.randint(-4,4)), 310.0,
                               random.uniform(-0.6,0.6), random.uniform(-1.4,-0.4), 255])
        for e in embers[:]:
            e[0]+=e[2]; e[1]+=e[3]; e[4]-=6
            if e[4]<=0: embers.remove(e)

        # Fundo estático
        tela.blit(_bg,(0,0))

        # Sprites reais do jogo como arte de capa
        # Inimigo à esquerda (escurecido levemente)
        ini_img = imgs_ini[0]
        ini_sc  = pygame.transform.scale(ini_img,
                    (int(ini_img.get_width()*1.35), int(ini_img.get_height()*1.35)))
        ini_x = 28; ini_y = CHAO_Y + off_ini[0] - ini_sc.get_height()
        tela.blit(ini_sc,(ini_x, ini_y))

        # Personagem à direita (virado para a esquerda, encarando o inimigo)
        ch_img  = imgs_char[0]
        ch_flip = pygame.transform.flip(ch_img, True, False)
        ch_sc   = pygame.transform.scale(ch_flip,
                    (int(ch_img.get_width()*1.5), int(ch_img.get_height()*1.5)))
        ch_x = LARGURA_TELA - 28 - ch_sc.get_width()
        ch_y = CHAO_Y + off_char[0] - ch_sc.get_height()
        tela.blit(ch_sc,(ch_x, ch_y))

        # Tochas animadas
        _tocha(tela, 125, 318, t)
        _tocha(tela, LARGURA_TELA-125, 318, t)

        # Brasas
        for e in embers:
            es = _ns(5,5)
            pygame.draw.circle(es,(255,180,50,max(0,e[4])),(2,2),2)
            tela.blit(es,(int(e[0]),int(e[1])))

        # ── FAIXA DO TÍTULO ──────────────────────────────────────
        band = pygame.Surface((700,168),pygame.SRCALPHA)
        band.fill((0,0,0,175))
        tela.blit(band,(50,58))
        # Borda dourada dupla
        pygame.draw.rect(tela,(170,110,15),(50,58,700,168),3)
        pygame.draw.rect(tela,(100,65,8),(54,62,692,160),1)
        # Ornamentos nos cantos
        for cx3,cy3 in [(50,58),(750,58),(50,226),(750,226)]:
            pygame.draw.circle(tela,(170,110,15),(cx3,cy3),6)

        # Linha separadora superior e inferior
        pygame.draw.line(tela,(200,140,20),(70,92),(730,92),1)
        pygame.draw.line(tela,(200,140,20),(70,222),(730,222),1)

        # ── TEXTO DO TÍTULO ──────────────────────────────────────
        # "FÚRIA DAS" — sombra + dourado
        for ox,oy,cor in [(4,4,(60,15,0)),(2,2,(130,50,5)),(0,0,(255,205,25))]:
            r1 = FM.render("FÚRIA DAS", True, cor)
            tela.blit(r1, r1.get_rect(center=(LARGURA_TELA//2+ox, 118+oy)))
        # "MASMORRAS" — maior, sombra + dourado com pulso
        pulse = int(abs(math.sin(t*0.04))*18)
        for ox,oy,cor in [(5,5,(50,10,0)),(3,3,(140,45,10)),(0,0,(255-pulse,195+pulse//3,20))]:
            r2 = FG.render("MASMORRAS", True, cor)
            tela.blit(r2, r2.get_rect(center=(LARGURA_TELA//2+ox, 182+oy)))

        # Tagline
        tag = FI.render("— Sobreviva. Lute. Conquiste. —", True, (155,115,50))
        tela.blit(tag, tag.get_rect(center=(LARGURA_TELA//2, 238)))

        # ── PAINEL DO MENU ───────────────────────────────────────
        pan = pygame.Surface((440,215),pygame.SRCALPHA)
        pan.fill((0,0,0,185))
        tela.blit(pan,(180,358))
        pygame.draw.rect(tela,(120,80,14),(180,358,440,215),2)

        txt(tela,"ESPAÇO  —  Iniciar Aventura",FM,BRANCO,LARGURA_TELA//2,400)
        txt(tela,"R  —  Recordes",FP,(180,180,160),LARGURA_TELA//2,442)
        txt(tela,"Q  —  Sair",FP,(180,180,160),LARGURA_TELA//2,476)
        txt(tela,"CTRL  Poder Especial       ALT  Bloquear",FI,(90,90,80),LARGURA_TELA//2,510)
        txt(tela,"ESC  Pausar",FI,(90,90,80),LARGURA_TELA//2,535)

        # Rodapé de controles
        txt(tela,"← →  Mover    ↑  Pular    ESPAÇO  Atacar    ALT  Bloquear",FI,(70,70,65),LARGURA_TELA//2,ALTURA_TELA-28)
        # Crédito do desenvolvedor
        dev_f = pygame.font.Font(None,24)
        dev_t = dev_f.render("Desenvolvido Por  Leandro Oliveira Moraes", True, (180,135,35))
        tela.blit(dev_t, dev_t.get_rect(center=(LARGURA_TELA//2, ALTURA_TELA-10)))

        pygame.display.flip(); clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_SPACE: return
                if ev.key==pygame.K_r: tela_rank()
                if ev.key==pygame.K_q: pygame.quit(); sys.exit()

def pausa():
    ov=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA); ov.fill((0,0,0,180))
    while True:
        tela.blit(ov,(0,0))
        txt(tela,"PAUSADO",FG,AMAR,LARGURA_TELA//2,200)
        txt(tela,"ESC / ESPAÇO  Continuar",FP,BRANCO,LARGURA_TELA//2,310)
        txt(tela,"R  Ranking",FP,BRANCO,LARGURA_TELA//2,355)
        txt(tela,"Q  Sair para o menu",FP,BRANCO,LARGURA_TELA//2,400)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key in(pygame.K_ESCAPE,pygame.K_SPACE): return True
                if ev.key==pygame.K_r: tela_rank()
                if ev.key==pygame.K_q: return False

def tela_rank():
    rk=load_rk()
    while True:
        tela.fill(CARVAO)
        txt(tela,"TOP 5 PONTUAÇÕES",FM,DOURO,LARGURA_TELA//2,100)
        if not rk: txt(tela,"Nenhum recorde ainda!",FP,CINZA,LARGURA_TELA//2,260)
        for i,r in enumerate(rk):
            c=[DOURO,CINZA,MARROM,BRANCO,BRANCO][i]
            txt(tela,f"{i+1}. {r.get('nome','?'):10s}  {r['pts']:>6} pts  Onda {r.get('onda',1)}",FP,c,LARGURA_TELA//2,180+i*50)
        txt(tela,"ESPAÇO  Voltar",FP,BRANCO,LARGURA_TELA//2,ALTURA_TELA-55)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key in(pygame.K_SPACE,pygame.K_ESCAPE): return

def game_over(pts,onda,nome):
    rk=salvar_rk(pts,onda,nome)
    pos=next((i+1 for i,r in enumerate(rk) if r["pts"]==pts),None)
    while True:
        tela.fill(PRETO)
        txt(tela,"GAME OVER",FG,VERM,LARGURA_TELA//2,140)
        txt(tela,f"Pontuação: {pts}",FM,BRANCO,LARGURA_TELA//2,240)
        txt(tela,f"Onda: {onda}",FP,AMAR,LARGURA_TELA//2,295)
        if pos: txt(tela,f"#{pos} no ranking!",FP,DOURO,LARGURA_TELA//2,340)
        txt(tela,"ESPAÇO  Jogar novamente",FP,BRANCO,LARGURA_TELA//2,415)
        txt(tela,"R  Ranking   Q  Sair",FP,BRANCO,LARGURA_TELA//2,460)
        pygame.display.flip()
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_SPACE: return True
                if ev.key==pygame.K_r: tela_rank()
                if ev.key==pygame.K_q: return False

def vitoria():
    t = 0
    while True:
        t += 1
        tela.fill(PRETO)
        for _ in range(4):
            pygame.draw.circle(tela,BRANCO,(random.randint(0,LARGURA_TELA),random.randint(0,ALTURA_TELA//2)),1)
        pulse = int(abs(math.sin(t*0.05))*20)
        txt(tela,"VITÓRIA!",FG,(255,215+pulse//4,20),LARGURA_TELA//2,150)
        txt(tela,"Você derrotou O Inimigo Final!",FM,BRANCO,LARGURA_TELA//2,270)
        txt(tela,"Fúria das Masmorras — Conquistada!",FP,DOURO,LARGURA_TELA//2,330)
        txt(tela,"ESPAÇO  Jogar novamente",FP,CIANO,LARGURA_TELA//2,440)
        txt(tela,"Q  Sair",FP,(180,180,160),LARGURA_TELA//2,490)
        pygame.display.flip(); clock.tick(FPS)
        for ev in pygame.event.get():
            if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
            if ev.type==pygame.KEYDOWN:
                if ev.key==pygame.K_SPACE: return True
                if ev.key==pygame.K_q: return False

# ═══════════════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════════════
def main():
    global personagem, inimigos_g, projeteis_g, shake_f, flash_a, flash_c
    menu_ini(); tp=tela_sel()
    FASE_FINAL_ONDA = 21

    while True:
        PTS=0; vidas=3; onda=1; mortos=0; lim=5; MAX=1
        cen=0; boss=None; boss_wave=False
        extra_boss_phase=-1; item_timer_extra=0
        vitoria_flag=False; vitoria_result=False
        bg_scroll=0.0
        inimigos_g=pygame.sprite.Group()
        itens_g=pygame.sprite.Group()
        projeteis_g=pygame.sprite.Group()
        personagem=Personagem(tp)
        for _ in range(4): itens_g.add(mk_item())
        tspawn=120
        tfs.clear(); parts.clear(); shake_f=0; flash_a=0
        tocar_cenario(0); rodando=True

        while rodando:
            for ev in pygame.event.get():
                if ev.type==pygame.QUIT: pygame.quit(); sys.exit()
                elif ev.type==pygame.KEYDOWN:
                    if ev.key==pygame.K_ESCAPE:
                        if not pausa(): rodando=False; break
                    elif ev.key==pygame.K_SPACE:
                        personagem.iniciar_atq(False)
                        alvos=list(inimigos_g)+(([boss]) if boss else [])
                        for a in alvos:
                            ok,d=personagem.atacar(a)
                            if ok:
                                add_tf(a.rect.centerx,a.rect.top-10,f"-{d}",LARAN)
                                if a.vida<=0:
                                    if isinstance(a,Inimigo):
                                        if a.comp=='morto_vivo' and not a.revived:
                                            a.revived=True; a.vida=a.vmax//2
                                            ri=a.image.copy(); ri.fill((160,220,160),special_flags=pygame.BLEND_RGB_MULT); a.image=ri
                                        else:
                                            if a.comp=='dividido' and not a.divided:
                                                a.divided=True
                                                for _ in range(2):
                                                    m=Inimigo(15); m.rect.center=a.rect.center
                                                    m.vel=6; m.vida=m.vmax=8; inimigos_g.add(m)
                                            if random.random()<.12 and len(itens_g)<6: itens_g.add(mk_item(a.rect.centerx))
                                            PTS+=10+personagem.combo*2; mortos+=1
                                            add_parts(a.rect.centerx,a.rect.centery,AMAR,10); a.kill()
                                    else:
                                        if isinstance(boss,BossFinalExtra):
                                            fi_v=boss.fi; PTS+=1000
                                            itens_g.add(mk_item(boss.rect.centerx)); itens_g.add(mk_item(boss.rect.centerx))
                                            add_tf(boss.rect.centerx,boss.rect.top-30,f"{boss.nome} ANIQUILADO!",DOURO,36)
                                            add_parts(boss.rect.centerx,boss.rect.centery,DOURO,30); boss=None
                                            if fi_v==4:
                                                pygame.mixer.music.stop()
                                                vitoria_flag=True; vitoria_result=vitoria(); rodando=False
                                            else:
                                                extra_boss_phase=fi_v+1
                                                boss=BossFinalExtra(extra_boss_phase); tocar_cenario(5,boss=True)
                                                add_tf(LARGURA_TELA//2,180,f"??? {boss.nome} ???",VERM,48)
                                        elif isinstance(boss,FinalBoss):
                                            fi_v=boss.fi; PTS+=500
                                            itens_g.add(mk_item(boss.rect.centerx))
                                            add_tf(boss.rect.centerx,boss.rect.top-30,"BOSS FINAL DERROTADO!",DOURO,36)
                                            add_parts(boss.rect.centerx,boss.rect.centery,DOURO,25); boss=None
                                            if fi_v==4:
                                                extra_boss_phase=0
                                                boss=BossFinalExtra(0); tocar_cenario(5,boss=True)
                                                add_tf(LARGURA_TELA//2,180,f"??? {boss.nome} ???",VERM,48)
                                            else: tocar_cenario(5)
                                        else:
                                            PTS+=200; itens_g.add(mk_item(boss.rect.centerx))
                                            add_tf(boss.rect.centerx,boss.rect.top-30,"BOSS DERROTADO!",DOURO,36)
                                            add_parts(boss.rect.centerx,boss.rect.centery,DOURO,20); boss=None; tocar_cenario(cen)
                    elif ev.key==pygame.K_LCTRL:
                        if personagem.mp<10:
                            add_tf(personagem.rect.centerx,personagem.rect.top,"SEM MP!",CIANO,30)
                        else:
                            personagem.mp-=10
                            personagem.iniciar_atq(True)
                            alvos=list(inimigos_g)+(([boss]) if boss else [])
                            for a in alvos:
                                ok,d=personagem.atacar_esp(a)
                                if ok:
                                    add_tf(a.rect.centerx,a.rect.top-10,f"-{d}!",CIANO,32)
                                    if a.vida<=0:
                                        if isinstance(a,Inimigo):
                                            if a.comp=='morto_vivo' and not a.revived:
                                                a.revived=True; a.vida=a.vmax//2
                                                ri=a.image.copy(); ri.fill((160,220,160),special_flags=pygame.BLEND_RGB_MULT); a.image=ri
                                            else:
                                                if random.random()<.12 and len(itens_g)<6: itens_g.add(mk_item(a.rect.centerx))
                                                PTS+=20+personagem.combo*5; mortos+=1
                                                add_parts(a.rect.centerx,a.rect.centery,CIANO,10); a.kill()
                                        else:
                                            if isinstance(boss,BossFinalExtra):
                                                fi_v=boss.fi; PTS+=1000
                                                itens_g.add(mk_item(boss.rect.centerx)); itens_g.add(mk_item(boss.rect.centerx))
                                                add_tf(boss.rect.centerx,boss.rect.top-30,f"{boss.nome} ANIQUILADO!",DOURO,36)
                                                add_parts(boss.rect.centerx,boss.rect.centery,DOURO,30); boss=None
                                                if fi_v==4:
                                                    pygame.mixer.music.stop()
                                                    vitoria_flag=True; vitoria_result=vitoria(); rodando=False
                                                else:
                                                    extra_boss_phase=fi_v+1
                                                    boss=BossFinalExtra(extra_boss_phase); tocar_cenario(5,boss=True)
                                                    add_tf(LARGURA_TELA//2,180,f"??? {boss.nome} ???",VERM,48)
                                            elif isinstance(boss,FinalBoss):
                                                fi_v=boss.fi; PTS+=500
                                                itens_g.add(mk_item(boss.rect.centerx))
                                                add_tf(boss.rect.centerx,boss.rect.top-30,"BOSS FINAL DERROTADO!",DOURO,36)
                                                add_parts(boss.rect.centerx,boss.rect.centery,DOURO,25); boss=None
                                                if fi_v==4:
                                                    extra_boss_phase=0
                                                    boss=BossFinalExtra(0); tocar_cenario(5,boss=True)
                                                    add_tf(LARGURA_TELA//2,180,f"??? {boss.nome} ???",VERM,48)
                                                else: tocar_cenario(5)
                                            else:
                                                PTS+=200; itens_g.add(mk_item(boss.rect.centerx))
                                                add_parts(boss.rect.centerx,boss.rect.centery,DOURO,20); boss=None; tocar_cenario(cen)

            if not rodando: break
            personagem.update()
            for e in list(inimigos_g): e.update()
            projeteis_g.update()
            if boss: boss.update()

            # Itens HP/MP mais frequentes durante os BossFinalExtra
            if isinstance(boss,BossFinalExtra) and len(itens_g)<8:
                item_timer_extra-=1
                if item_timer_extra<=0:
                    item_timer_extra=random.randint(100,180)
                    itens_g.add(mk_item(sub=random.choice(['pocao','pocao','mp10','mp20','mp50'])))

            for p in list(projeteis_g):
                if p.rect.colliderect(personagem.rect):
                    personagem.dano(p.dano); add_parts(p.rect.centerx,p.rect.centery,LARAN); p.kill()

            for it in pygame.sprite.spritecollide(personagem,itens_g,True):
                it.aplicar(personagem,inimigos_g); PTS+=5
                if len(itens_g)<4 and random.random()<.5: itens_g.add(mk_item())

            while mortos>=lim:
                onda+=1; lim+=onda*3; MAX=min(3,1+(onda-1)//2); PTS+=onda*20
                personagem.curar(20); add_tf(LARGURA_TELA//2,200,f"ONDA {onda}!",AMAR,42)
                nc=idx_cen(onda)
                if nc!=cen:
                    cen=nc; boss_wave=False
                    if cen==5: tocar_cenario(5)
                elif onda>=FASE_FINAL_ONDA: boss_wave=False

            if onda<FASE_FINAL_ONDA:
                if onda%5==0 and not boss_wave and boss is None:
                    boss_wave=True; bi=min(4,(onda//5)-1)
                    boss=Boss(bi); tocar_cenario(cen,boss=True)
                    add_tf(LARGURA_TELA//2,180,f"BOSS: {boss.nome}!",VERM,44)
            else:
                fi_spawn=onda-FASE_FINAL_ONDA
                if not boss_wave and boss is None and fi_spawn<5:
                    boss_wave=True
                    boss=FinalBoss(fi_spawn); tocar_cenario(5,boss=True)
                    add_tf(LARGURA_TELA//2,180,f"BOSS FINAL: {boss.nome}!",VERM,48)

            if boss is None and len(inimigos_g)<MAX:
                tspawn-=1
                if tspawn<=0:
                    dif=1.0+(onda-1)*.25
                    tp_=random.randint(1,min(63,2+onda*2))
                    inimigos_g.add(Inimigo(tp_,dif)); tspawn=max(60,180-onda*15)

            if personagem.vida<=0:
                if vidas>1:
                    vidas-=1; personagem.vida=personagem.VMAX; personagem.inv=120
                    flash_a=200; flash_c=BRANCO
                    add_tf(LARGURA_TELA//2,250,f"VIDA PERDIDA! {vidas} restantes",VERM,32)
                else: rodando=False

            for t_ in tfs[:]:
                t_.update()
                if not t_.vivo: tfs.remove(t_)
            for p in parts[:]:
                p.update()
                if not p.vivo: parts.remove(p)
            if shake_f>0: shake_f-=1
            if flash_a>0: flash_a=max(0,flash_a-8)

            # ── RENDER ──
            sx=random.randint(-5,5) if shake_f>0 else 0
            sy=random.randint(-5,5) if shake_f>0 else 0
            # parallax: fundo desloca suavemente com a posição do personagem
            bg_target=-(personagem.rect.centerx/LARGURA_TELA)*(BG_W-LARGURA_TELA)
            bg_scroll+=(bg_target-bg_scroll)*0.05
            tela.fill(PRETO)
            tela.blit(FUNDOS[cen],(int(bg_scroll)+sx,sy))

            for it in itens_g: tela.blit(it.image,(it.rect.x+sx,it.rect.y+sy))

            for e in inimigos_g:
                img=pygame.transform.flip(e.image,True,False) if e.dir else e.image
                if e.flash>0:
                    fl=img.copy(); fl.fill((200,200,200),special_flags=pygame.BLEND_RGB_ADD); img=fl
                if e.fatq>0:
                    lx=28 if e.dir else -28; w,h=img.get_width(),img.get_height()
                    ia=pygame.transform.scale(img,(int(w*1.45),int(h*1.45)))
                    ra=ia.get_rect(midbottom=(e.rect.centerx+lx+sx,e.rect.bottom+sy)); tela.blit(ia,ra.topleft)
                else: tela.blit(img,(e.rect.x+sx,e.rect.y+sy))
                if e.comp=='fantasma' and e.inv_fant:
                    gv=_ns(e.rect.width+10,e.rect.height+10)
                    pygame.draw.ellipse(gv,(140,180,255,60),(0,0,e.rect.width+10,e.rect.height+10))
                    tela.blit(gv,(e.rect.x-5+sx,e.rect.y-5+sy))
                e.draw_hp(tela)

            if boss:
                bi2=pygame.transform.flip(boss.image,True,False) if boss.dir else boss.image
                if boss.flash>0:
                    fl=bi2.copy(); fl.fill((200,200,200),special_flags=pygame.BLEND_RGB_ADD); bi2=fl
                if boss.fatq>0:
                    lx=35 if boss.dir else -35; w,h=bi2.get_width(),bi2.get_height()
                    ba=pygame.transform.scale(bi2,(int(w*1.5),int(h*1.5)))
                    rb=ba.get_rect(midbottom=(boss.rect.centerx+lx+sx,boss.rect.bottom+sy)); tela.blit(ba,rb.topleft)
                else: tela.blit(bi2,(boss.rect.x+sx,boss.rect.y+sy))

            for p in projeteis_g: tela.blit(p.image,(p.rect.x+sx,p.rect.y+sy))
            personagem.desenhar(tela)
            for t_ in tfs: t_.draw(tela)
            for p in parts: p.draw(tela)

            if flash_a>0:
                fs=pygame.Surface((LARGURA_TELA,ALTURA_TELA),pygame.SRCALPHA)
                fs.fill(flash_c+(flash_a,)); tela.blit(fs,(0,0))

            hud(personagem,vidas,PTS,onda,boss)
            pygame.display.flip(); clock.tick(FPS)

        pygame.mixer.music.stop()
        if vitoria_flag:
            if vitoria_result: menu_ini(); tp=tela_sel()
            else: break
            continue
        nome=DADOS_CHAR[tp]["nome"]
        if not game_over(PTS,onda,nome): break
        tp=tela_sel()
    pygame.quit()

if __name__=="__main__":
    main()
