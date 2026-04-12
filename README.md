# Fúria das Masmorras

Beat 'em up 2D de ação e sobrevivência construído do zero com Python e pygame. Enfrente ondas crescentes de inimigos, derrote bosses épicos e chegue o mais longe possível — cada partida é um desafio novo.

---

## Rodando o jogo

**Dependência única:** pygame 2.x

```bash
pip install pygame
```

```bash
cd masmorra
python "import pygame.py"
```

---

## Controles

| Tecla | Ação |
|-------|------|
| `← →` | Mover |
| `↑` | Pular |
| `Espaço` | Atacar (combo encadeado) |
| `E` | Poder especial |
| `ESC` | Pausar |
| `R` | Ranking |
| `Q` | Sair |

---

## Personagens

Três estilos de jogo completamente distintos. A escolha muda a estratégia inteira:

| Personagem | Estilo | HP | Vel | Dano | Alcance |
|------------|--------|----|-----|------|---------|
| **Guerreiro** | Equilibrado — bom em tudo | 100 | 5 | 10 | 70 |
| **Mago** | Mata rápido, morre rápido | 70 | 4 | 20 | 130 |
| **Ladino** | Velocidade acima de tudo | 80 | 8 | 8 | 55 |

### Armas e poderes especiais

Cada personagem tem arma e poder especial únicos:

| Personagem | Ataque normal | Poder especial (`E`) |
|------------|--------------|----------------------|
| **Guerreiro** | Machado giratório | 5 machados orbitando em volta do personagem |
| **Mago** | Cajado + orbe mágico pulsante | 6 chamas azuis orbitando em volta do personagem |
| **Ladino** | Espada em arco de slash | 5 espadas orbitando em volta do personagem |

---

## Como o jogo funciona

### Ondas e progressão
O jogo é infinito em teoria — as ondas não têm fim e a dificuldade escala continuamente. Cada onda elimianda recupera 20 HP e dá bônus de pontuação. Inimigos ficam mais rápidos, mais resistentes e mais numerosos conforme as ondas avançam.

### Sistema de combo
Três ataques em sequência ativam o **Golpe Devastador**: o terceiro hit causa o dobro do dano normal. O tempo entre golpes precisa ser curto — o encadeamento se quebra se você hesitar.

### Bosses
A cada cinco ondas, a música muda e um Boss entra em cena. Cada boss tem três fases — ao perder HP, fica mais agressivo e rápido. Derrotá-lo vale pontuação alta e garante um item no chão.

| Boss | HP | Ataque especial |
|------|----|----------------|
| Dragão | 400 | Rajada de fogo |
| Cavaleiro Sombrio | 500 | Carga devastadora |
| Mago Maligno | 350 | Projéteis mágicos |
| Lorde Demônio | 600 | Explosão de projéteis |
| Deus do Caos | 800 | Ataque total |

### Fase Final

A partir da onda 21 começa a **Fase Final** — o cenário muda e cinco bosses supremos surgem em sequência, um por onda, cada um mais poderoso que o anterior:

| Boss final | HP | Estilo |
|------------|----|--------|
| Hydra das Trevas | 600 | Fogo |
| Senhor da Escuridão | 700 | Carga |
| Arauto do Caos | 800 | Mágico |
| Protetor Amaldiçoado | 900 | Caos |
| **O Inimigo Final** | **1200** | **Ultimate** |

Derrotar O Inimigo Final encerra o jogo com a tela de **Vitória**.

### Vidas
Três vidas por partida. Ao zerar o HP, uma vida é consumida e o HP é completamente restaurado. Quando a última vida acaba, vai para o Game Over.

---

## Inimigos

22 tipos, cada um com comportamento próprio. Não é só "vai na direção do jogador":

| Tipo | O que faz |
|------|-----------|
| Atirador | Mantém distância e atira projéteis |
| Carregador | Faz cargas rápidas quando está perto |
| Fantasma | Fica imune periodicamente |
| Berserker | Acelera muito quando com pouco HP |
| Curandeiro | Regenera os aliados próximos |
| Gigante | Lento e tanque — pisada que chacoalha o chão e empurra o jogador |
| Assassino | Teletransporta atrás do jogador |
| Bloqueador | Reduz dano recebido de frente |
| Morto-Vivo | Ressuscita uma vez com metade do HP |
| Dividido | Ao morrer, vira dois inimigos menores |

---

## Itens

Inimigos têm 25% de chance de dropar algo ao morrer. Caminhe em cima para coletar automaticamente.

| Item | Efeito |
|------|--------|
| Poção | +25 HP |
| Poção Forte | +50 HP |
| Bomba | 40 de dano em todos os inimigos na tela |

---

## Cenários

O cenário troca sozinho conforme a onda progride, com música própria para cada ambiente:

| Ondas | Cenário |
|-------|---------|
| 1 – 4 | Masmorra |
| 5 – 9 | Floresta |
| 10 – 14 | Castelo |
| 15 – 19 | Vulcão |
| 20 | Céu |
| 21+ | Fase Final |

Durante os bosses a música muda para a trilha de batalha. Se um arquivo de música não for encontrado, o jogo cai automaticamente para `musica_fundo.mp3` — sem crash, sem interrupção.

---

## Ranking

As cinco melhores pontuações ficam salvas em `ranking.json`. Acessível pelo menu principal, pela tela de pausa ou pelo Game Over.

---

## Arquivos do projeto

```
masmorra/
├── import pygame.py        # Código principal
├── ranking.json            # Recordes (gerado automaticamente)
│
├── personagem.png          # Guerreiro
├── inimigo.png – inimigo12.png   # Inimigos 1–12
├── item.png                # Sprite dos itens
├── machado.png             # Arma do jogador
├── fundo.jpg               # Cenário da masmorra
│
├── ataque.wav              # Som de ataque
├── colisao.wav             # Som de dano
├── coleta.wav              # Som de coleta de item
├── pulo.wav                # Som de pulo
└── musica_fundo.mp3        # Música padrão / fallback
```

**Arquivos opcionais** — o jogo gera tudo proceduralmente se não encontrar:

```
personagem_mago.png / personagem_ladino.png
boss1.png … boss5.png
inimigo13.png … inimigo22.png
item_bota.png / item_bomba.png / bomba.wav
musica_dungeon.mp3 / musica_floresta.mp3 / musica_castelo.mp3
musica_vulcao.mp3 / musica_ceu.mp3 / musica_boss.mp3
```

---

## Stack

- **Python 3.10+**
- **pygame 2.x**
- Persistência local via **JSON**
- Áudio: **WAV** (efeitos) + **MP3** (trilha)

---

**Desenvolvido por Leandro Oliveira Moraes**
