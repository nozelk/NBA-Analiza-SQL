from bottle import Bottle, request, template, static_file, TEMPLATE_PATH
from database import get_db
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import re

team_app = Bottle()



TEAM_STATS = ["WIN_percent", "FGM", "FGA", "FG_percent", "FTM", "FTA", 
              "FT_percent", "FG3M", "FG3A", "FG3_percent", "OREB", 
              "DREB", "REB", "AST", "PF", "STL", "TOV", "BLK", "PTS"]

def sanitize_filename(name):
    return re.sub(r'[^a-zA-Z0-9_]', '', name.replace(" ", "_"))

@team_app.route('/')
def team_analysis():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT full_name FROM teams")
        teams = [row[0] for row in cursor.fetchall()]
        conn.close()
        return template('team_analysis', teams=teams, stats=TEAM_STATS)
    except Exception as e:
        return f"Error: {str(e)}"

@team_app.route('/graph')
def team_graph():
    try:
        team = request.query.team
        stats = request.query.getall('stats')
        start_year = int(request.query.start_year)
        end_year = int(request.query.end_year)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM teams WHERE full_name=?", (team,))
        team_id = cursor.fetchone()[0]

        graphs = []
        for stat in stats:
            cursor.execute(f'''
                SELECT year, "{stat}" FROM team_stats 
                WHERE team_id=? AND year BETWEEN ? AND ?
                ORDER BY year
            ''', (team_id, start_year, end_year))
            data = cursor.fetchall()
            
            if not data:
                continue

            x = [row[0] for row in data]
            y = [row[1] for row in data]

            plt.figure(figsize=(12, 6))
            plt.plot(x, y, 'o-', linewidth=2, label=team)
            
            cursor.execute(f'''
                SELECT AVG("{stat}"), MAX("{stat}"), MIN("{stat}") 
                FROM team_stats WHERE year BETWEEN ? AND ?
            ''', (start_year, end_year))
            avg, maks, minv = cursor.fetchone()
            
            plt.axhline(avg, color='orange', linestyle='--', label='Povprečje')
            plt.axhline(maks, color='green', linestyle=':', label='Maksimum')
            plt.axhline(minv, color='red', linestyle=':', label='Minimum')
            
            plt.title(f"{stat} - {team}")
            plt.xlabel("Leto")
            plt.ylabel(stat.replace('_', ' ').title())
            plt.legend()
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

@team_app.route('/logo/<team>')
def team_logo(team):
    clean_name = sanitize_filename(team)
    file_path = f"./static/images/logos/{clean_name}.png"
    print(f"Looking for logo: {file_path}")

    return static_file(f"{clean_name}.png", root='./static/images/logos/')