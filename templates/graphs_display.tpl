% rebase('base.tpl')
<div class="container mt-4">
    % for graph in graphs:
    <div class="card mb-4 shadow">
        <div class="card-body">
            <img src="data:image/png;base64,{{graph}}" class="img-fluid">
        </div>
    </div>
    % end
    <a href="javascript:history.back()" class="btn btn-secondary mb-4">
        ← Nazaj
    </a>
</div>