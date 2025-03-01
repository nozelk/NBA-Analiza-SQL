from bottle import Bottle, request, template, static_file, response, TEMPLATE_PATH
from database import get_db
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re

player_app = Bottle()


PLAYER_STATS = ["FGM", "FGA", "FG_percent", "FTM", "FTA", "FT_percent", 
                "FG3M", "FG3A", "FG3_percent", "OREB", "DREB", "REB", 
                "AST", "PF", "STL", "TOV", "BLK", "PTS", "SALARY"]

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(" ", "_").replace("č", "c").replace("ć", "c"))

@player_app.route('/')
def player_analysis():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM players")
        players = [row[0] for row in cursor.fetchall()]
        conn.close()
        return template('player_analysis', players=players, stats=PLAYER_STATS)
    except Exception as e:
        return f"Error: {str(e)}"

@player_app.route('/graph')
def player_graph():
    try:
        player = request.query.player
        stats = request.query.getall('stats')
        start_year = int(request.query.start_year)
        end_year = int(request.query.end_year)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM players WHERE name=?", (player,))
        player_id = cursor.fetchone()[0]

        graphs = []
        for stat in stats:
            cursor.execute(f'''
                SELECT year, "{stat}" FROM player_stats 
                WHERE player_id=? AND year BETWEEN ? AND ?
                ORDER BY year
            ''', (player_id, start_year, end_year))
            data = cursor.fetchall()
            
            if not data:
                continue

            x = [row[0] for row in data]
            y = [row[1] for row in data]

            plt.figure(figsize=(12, 6))
            if 'percent' in stat.lower():
                plt.plot(x, y, 'o-', linewidth=2)
                plt.ylim(0, 100)
            else:
                plt.bar(x, y, alpha=0.7)
            
            plt.title(f"{stat} - {player}")
            plt.xlabel("Leto")
            plt.ylabel(stat.replace('_', ' ').title())
            plt.grid(True, linestyle='--', alpha=0.7)
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            plt.close()
            graphs.append(base64.b64encode(buffer.getvalue()).decode())

        return template('graphs_display', graphs=graphs)
    
    except Exception as e:
        return f"Napaka: {str(e)}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

@player_app.route('/image/<player>')
def player_image(player):
    clean_name = sanitize_filename(player)
    return static_file(f"{clean_name}.png", root='./static/images/players/')