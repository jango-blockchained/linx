frappe.pages['collector'].on_page_load = function(wrapper) {
    var page = frappe.ui.make_app_page({
        parent: wrapper,
        title: 'Crypto Data Collection',
        single_column: true
    });

    $(page.body).append(`
        <div>
            <select id="endpoint-select" class="form-control">
                <option value="simple">Simple</option>
                <option value="coins">Coins</option>
                <option value="contract">Contract</option>
                <option value="asset_platforms">Asset Platforms</option>
                <option value="coins/categories">Coins Categories</option>
                <option value="nfts">NFTs</option>
                <option value="onchain">Onchain</option>
                <option value="exchanges">Exchanges</option>
                <option value="derivatives">Derivatives</option>
                <option value="search">Search</option>
                <option value="search/trending">Search Trending</option>
                <option value="global">Global</option>
                <option value="companies">Companies</option>
            </select>
            <button class="btn btn-primary" id="collect-data">Collect Data</button>
            <pre id="data-output"></pre>
            <div id="data-table"></div>
            <div id="endpoint-status-table"></div>
        </div>
    `);

    $('#collect-data').on('click', function() {
        let endpoint = $('#endpoint-select').val();
        frappe.call({
            method: 'linx.linx.page.collector.collector.collect_data',
            args: {
                endpoint: endpoint
            },
            callback: function(response) {
                $('#data-output').text(response.message);
                fetchData(endpoint); // Fetch and display data after collection
                updateEndpointStatusTable(); // Update endpoint status table after collection
            }
        });
    });

    function fetchData(endpoint) {
        frappe.call({
            method: 'linx.linx.page.collector.collector.fetch_data',
            args: {
                endpoint: endpoint
            },
            callback: function(response) {
                if(response.message) {
                    let data = response.message;
                    let keys = Object.keys(data[0] || {});
                    let table = `<table class="table table-bordered">
                                    <thead>
                                        <tr>`;
                    keys.forEach(key => {
                        table += `<th>${key}</th>`;
                    });
                    table += `</tr>
                            <tbody>`;
                    data.forEach(row => {
                        table += `<tr>`;
                        keys.forEach(key => {
                            table += `<td>${row[key]}</td>`;
                        });
                        table += `</tr>`;
                    });
                    table += `</tbody></table>`;
                    $('#data-table').html(table);
                }
            }
        });
    }

    function updateEndpointStatusTable() {
        frappe.call({
            method: 'linx.linx.page.collector.collector.get_endpoint_status',
            callback: function(response) {
                if(response.message) {
                    let endpoints = response.message;
                    let table = `<table class="table table-bordered">
                                    <thead>
                                        <tr>
                                            <th>Endpoint</th>
                                            <th>File Loaded</th>
                                            <th>Last Collection Date</th>
                                        </tr>
                                    </thead>
                                    <tbody>`;
                    endpoints.forEach(endpoint => {
                        table += `<tr>
                                    <td>${endpoint.endpoint}</td>
                                    <td>${endpoint.file_loaded ? 'Yes' : 'No'}</td>
                                    <td>${endpoint.last_collection_date || '-'}</td>
                                  </tr>`;
                    });
                    table += `</tbody></table>`;
                    $('#endpoint-status-table').html(table);
                }
            }
        });
    }

    // Initial load of endpoint status table
    updateEndpointStatusTable();
};
