# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

J.A.R.V.I.S est un bot Discord Python (discord.py 2.7.1 / Python 3.12) qui gère des annonces de stream Twitch et l'attribution automatique de rôles à l'arrivée de nouveaux membres.

## Commands

```bash
# Activer l'environnement virtuel
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le bot
python main.py
```

## Architecture

### Entry point — `main.py`
Crée le bot, charge dynamiquement tous les fichiers `.py` dans `cogs/`, et appelle `init_db()` au démarrage (`on_ready`).

### Configuration — `config.py`
Centralise toutes les variables d'environnement depuis `.env`. Toute nouvelle constante de config doit être ajoutée ici, jamais lue directement avec `os.getenv` dans les cogs.

### Logging — `logger.py`
Usine de loggers : appeler `setup_logger("nom_du_module")` en haut de chaque fichier pour obtenir un logger nommé avec format uniforme.

### Base de données — `database/`
- `connection.py` : `get_db()` retourne une connexion `aiosqlite` avec `row_factory`
- `models.py` : `init_db()` crée les tables au démarrage. Ajouter les nouveaux `CREATE TABLE IF NOT EXISTS` ici.

Table existante : `conversations(id, user_id, user_name, role, content, channel_id, created_at)`

### Cogs — `cogs/`
Chaque fichier est un module de fonctionnalité chargé automatiquement. Chaque cog doit exposer `async def setup(bot)`.

- **`twitch.py`** : poll l'API Twitch toutes les 2 min via une `@tasks.loop`. Gère le state `is_live` pour n'envoyer l'annonce qu'une seule fois par live. Récupère un token OAuth à chaque vérification.
- **`welcome.py`** : écoute `on_member_join`. Attribue automatiquement le rôle configuré (`MEMBER_ROLE_NAME`) à chaque nouveau membre.

## Environment variables

Copier `.env.example` → `.env` et renseigner :

| Variable | Rôle |
|---|---|
| `DISCORD_TOKEN` | Token du bot Discord |
| `TWITCH_CLIENT_ID` / `TWITCH_CLIENT_SECRET` | Credentials Twitch API |
| `TWITCH_STREAMER` | Login Twitch à surveiller (défaut : `drykai_`) |
| `TWITCH_ANNOUNCE_CHANNEL` | ID du salon Discord d'annonce Twitch |
| `MEMBER_ROLE_NAME` | Nom du rôle à attribuer aux nouveaux membres (défaut : `membre`) |

## Adding a new cog

1. Créer `cogs/mon_cog.py` avec une classe héritant de `commands.Cog`
2. Ajouter `async def setup(bot): await bot.add_cog(MonCog(bot))` à la fin
3. Le bot le chargera automatiquement au prochain démarrage
