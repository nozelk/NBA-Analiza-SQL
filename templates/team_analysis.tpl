% rebase('base.tpl')
<div class="card shadow">
    <div class="card-body">
        <h2 class="card-title mb-4">Analiza ekip</h2>
        
        <form action="/team/graph" method="get" class="row g-3">
            <!-- Izbira ekipe -->
            <div class="col-md-4">
                <label class="form-label">Izberi ekipo:</label>
                <select name="team" class="form-select" onchange="updateLogo(this.value)">
                    % for team in teams:
                        <option value="{{team}}">{{team}}</option>
                    % end
                </select>
            </div>

            <!-- Prikaz logotipa -->
            <div class="col-md-2">
                <img id="team-logo" src="/team/logo/{{teams[0]}}" 
                     class="img-fluid mt-2" 
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
                               value="2004" min="2004" max="2023">
                    </div>
                    <div class="col">
                        <label class="form-label">Do leta:</label>
                        <input type="number" name="end_year" 
                               class="form-control" 
                               value="2023" min="2004" max="2023">
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
function updateLogo(team) {
    document.getElementById('team-logo').src = `/team/logo/${encodeURIComponent(team)}`;
}
</script>