% rebase('base.tpl')
<div class="card shadow">
    <div class="card-body">
        <h2 class="card-title mb-4">Analiza igralcev</h2>
        
        <form action="/player/graph" method="get" class="row g-3">
            <!-- Izbira igralca -->
            <div class="col-md-4">
                <label class="form-label">Izberi igralca:</label>
                <select name="player" class="form-select" onchange="updateImage(this.value)">
                    % for player in players:
                        <option value="{{player}}">{{player}}</option>
                    % end
                </select>
            </div>

            <!-- Prikaz slike -->
            <div class="col-md-2">
                <img id="player-image" src="/player/image/{{players[0]}}" 
                     class="img-fluid mt-2 rounded-circle" 
                     style="max-height: 100px">
            </div>

            <!-- Izbira statistik -->
            <div class="col-md-12">
                <label class="form-label">Statistike:</label>
                <div class="row">
                    % for stat in stats:
                    <div class="col-4 col-md-3">
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" 
                                   name="stats" value="{{stat}}" id="{{stat}}">
                            <label class="form-check-label" for="{{stat}}">
                                {{stat}}
                            </label>
                        </div>
                    </div>
                    % end
                </div>
            </div>

            <!-- Letniški razpon -->
            <div class="col-md-6">
                <div class="row">
                    <div class="col">
                        <label class="form-label">Od leta:</label>
                        <input type="number" name="start_year" 
                               class="form-control" 
                               value="2010" min="2000" max="2023">
                    </div>
                    <div class="col">
                        <label class="form-label">Do leta:</label>
                        <input type="number" name="end_year" 
                               class="form-control" 
                               value="2023" min="2000" max="2023">
                    </div>
                </div>
            </div>

            <div class="col-12">
                <button type="submit" class="btn btn-success">
                    Generiraj grafe
                </button>
            </div>
        </form>
    </div>
</div>

<script>
function updateImage(player) {
    const cleanName = player.replace(/ /g, '_').replace(/č/g, 'c').replace(/ć/g, 'c');
    document.getElementById('player-image').src = `/player/image/${encodeURIComponent(cleanName)}`;
}
</script>