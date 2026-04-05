# # app.py
# from flask import Flask, render_template_string, jsonify, request
# import pandas as pd
# import os
# from datetime import datetime
# import re
#
# app = Flask(__name__)
#
# # HTML Template with posting time and recent ads section
# HTML_TEMPLATE = """
# <!DOCTYPE html>
# <html lang="en">
# <head>
#     <meta charset="UTF-8">
#     <meta name="viewport" content="width=device-width, initial-scale=1.0">
#     <title>Real Estate Lead Engine Dashboard</title>
#     <style>
#         * {
#             margin: 0;
#             padding: 0;
#             box-sizing: border-box;
#         }
#
#         body {
#             font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
#             background: #f0f2f5;
#             padding: 20px;
#         }
#
#         .container {
#             max-width: 1400px;
#             margin: 0 auto;
#         }
#
#         /* Header */
#         .header {
#             background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
#             padding: 20px;
#             border-radius: 10px;
#             color: white;
#             margin-bottom: 20px;
#         }
#
#         .header h1 {
#             font-size: 24px;
#             margin-bottom: 5px;
#         }
#
#         .header p {
#             opacity: 0.9;
#             font-size: 14px;
#         }
#
#         /* Stats Grid */
#         .stats-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
#             gap: 15px;
#             margin-bottom: 20px;
#         }
#
#         .stat-card {
#             background: white;
#             padding: 15px;
#             border-radius: 10px;
#             text-align: center;
#             box-shadow: 0 1px 3px rgba(0,0,0,0.1);
#         }
#
#         .stat-number {
#             font-size: 28px;
#             font-weight: bold;
#             color: #667eea;
#         }
#
#         .stat-label {
#             color: #666;
#             font-size: 12px;
#             margin-top: 5px;
#         }
#
#         /* Recent Ads Section */
#         .recent-section {
#             background: white;
#             border-radius: 10px;
#             padding: 15px;
#             margin-bottom: 20px;
#             box-shadow: 0 1px 3px rgba(0,0,0,0.1);
#         }
#
#         .recent-title {
#             font-size: 18px;
#             font-weight: bold;
#             margin-bottom: 15px;
#             color: #333;
#             border-left: 4px solid #667eea;
#             padding-left: 12px;
#         }
#
#         .recent-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
#             gap: 12px;
#         }
#
#         .recent-item {
#             display: flex;
#             align-items: center;
#             padding: 10px;
#             background: #f8f9fa;
#             border-radius: 8px;
#             transition: all 0.2s;
#         }
#
#         .recent-item:hover {
#             background: #e9ecef;
#             transform: translateX(3px);
#         }
#
#         .recent-icon {
#             font-size: 24px;
#             margin-right: 12px;
#         }
#
#         .recent-info {
#             flex: 1;
#         }
#
#         .recent-info .title {
#             font-weight: bold;
#             font-size: 13px;
#             margin-bottom: 4px;
#             color: #333;
#         }
#
#         .recent-info .price {
#             color: #e74c3c;
#             font-weight: bold;
#             font-size: 12px;
#         }
#
#         .recent-info .phone {
#             color: #27ae60;
#             font-size: 11px;
#         }
#
#         .recent-time {
#             text-align: right;
#             font-size: 10px;
#             color: #999;
#         }
#
#         .time-badge {
#             background: #e8f4f8;
#             padding: 2px 8px;
#             border-radius: 12px;
#             font-size: 10px;
#             display: inline-block;
#         }
#
#         /* Filters */
#         .filters {
#             background: white;
#             padding: 15px;
#             border-radius: 10px;
#             margin-bottom: 20px;
#             display: flex;
#             flex-wrap: wrap;
#             gap: 10px;
#             align-items: center;
#         }
#
#         .filter-group {
#             display: flex;
#             align-items: center;
#             gap: 8px;
#         }
#
#         .filter-group label {
#             font-size: 12px;
#             font-weight: bold;
#             color: #555;
#         }
#
#         select, input {
#             padding: 6px 10px;
#             border: 1px solid #ddd;
#             border-radius: 5px;
#             font-size: 12px;
#         }
#
#         button {
#             background: #667eea;
#             color: white;
#             border: none;
#             padding: 6px 15px;
#             border-radius: 5px;
#             cursor: pointer;
#             font-size: 12px;
#         }
#
#         button:hover {
#             background: #5a67d8;
#         }
#
#         /* Leads Grid */
#         .leads-grid {
#             display: grid;
#             grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
#             gap: 15px;
#             margin-top: 15px;
#         }
#
#         .lead-card {
#             background: white;
#             border-radius: 8px;
#             overflow: hidden;
#             box-shadow: 0 1px 3px rgba(0,0,0,0.1);
#             transition: transform 0.2s;
#         }
#
#         .lead-card:hover {
#             transform: translateY(-2px);
#             box-shadow: 0 4px 12px rgba(0,0,0,0.15);
#         }
#
#         .lead-image {
#             height: 160px;
#             background: #f5f5f5;
#             display: flex;
#             align-items: center;
#             justify-content: center;
#             overflow: hidden;
#         }
#
#         .lead-image img {
#             width: 100%;
#             height: 100%;
#             object-fit: cover;
#         }
#
#         .lead-info {
#             padding: 12px;
#         }
#
#         .lead-title {
#             font-size: 13px;
#             font-weight: bold;
#             margin-bottom: 8px;
#             height: 36px;
#             overflow: hidden;
#             color: #333;
#         }
#
#         .lead-price {
#             color: #e74c3c;
#             font-weight: bold;
#             font-size: 16px;
#             margin-bottom: 6px;
#         }
#
#         .lead-phone {
#             color: #27ae60;
#             font-weight: bold;
#             font-size: 13px;
#             margin-bottom: 6px;
#         }
#
#         .lead-location {
#             font-size: 11px;
#             color: #666;
#             margin-bottom: 6px;
#         }
#
#         .lead-seller {
#             font-size: 11px;
#             color: #8e44ad;
#             margin-bottom: 6px;
#         }
#
#         .lead-posted {
#             font-size: 10px;
#             color: #999;
#             margin-top: 6px;
#             display: flex;
#             justify-content: space-between;
#             align-items: center;
#         }
#
#         .lead-link {
#             font-size: 11px;
#             margin-top: 8px;
#         }
#
#         .lead-link a {
#             color: #3498db;
#             text-decoration: none;
#         }
#
#         .lead-link a:hover {
#             text-decoration: underline;
#         }
#
#         .badge {
#             display: inline-block;
#             padding: 2px 8px;
#             border-radius: 4px;
#             font-size: 10px;
#             font-weight: bold;
#             margin-right: 5px;
#         }
#
#         .badge-furnished {
#             background: #d4edda;
#             color: #155724;
#         }
#
#         .badge-unfurnished {
#             background: #f8d7da;
#             color: #721c24;
#         }
#
#         .badge-new {
#             background: #ffc107;
#             color: #856404;
#         }
#
#         /* Pagination */
#         .pagination {
#             display: flex;
#             justify-content: center;
#             gap: 8px;
#             margin-top: 20px;
#             flex-wrap: wrap;
#         }
#
#         .page-btn {
#             background: white;
#             color: #333;
#             border: 1px solid #ddd;
#             padding: 6px 12px;
#             min-width: 36px;
#         }
#
#         .page-btn.active {
#             background: #667eea;
#             color: white;
#             border-color: #667eea;
#         }
#
#         .page-btn:hover:not(.active) {
#             background: #f0f0f0;
#         }
#
#         .loading {
#             text-align: center;
#             padding: 40px;
#             color: #666;
#         }
#
#         .no-results {
#             text-align: center;
#             padding: 40px;
#             color: #999;
#         }
#
#         .footer {
#             text-align: center;
#             padding: 20px;
#             font-size: 11px;
#             color: #999;
#             margin-top: 20px;
#         }
#
#         @media (max-width: 768px) {
#             body {
#                 padding: 10px;
#             }
#             .leads-grid {
#                 grid-template-columns: 1fr;
#             }
#             .filters {
#                 flex-direction: column;
#                 align-items: stretch;
#             }
#             .recent-grid {
#                 grid-template-columns: 1fr;
#             }
#         }
#     </style>
# </head>
# <body>
#     <div class="container">
#         <div class="header">
#             <h1>🏠 Real Estate Lead Engine</h1>
#             <p>Professional Lead Management Dashboard</p>
#         </div>
#
#         <div class="stats-grid" id="stats">
#             <div class="stat-card">
#                 <div class="stat-number">-</div>
#                 <div class="stat-label">Total Leads</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-number">-</div>
#                 <div class="stat-label">With Phone</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-number">-</div>
#                 <div class="stat-label">Unique Locations</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-number">-</div>
#                 <div class="stat-label">Furnished</div>
#             </div>
#             <div class="stat-card">
#                 <div class="stat-number">-</div>
#                 <div class="stat-label">Recent (24h)</div>
#             </div>
#         </div>
#
#         <!-- Recent Ads Section -->
#         <div class="recent-section" id="recentSection">
#             <div class="recent-title">🕐 Recently Posted Ads</div>
#             <div id="recentAds" class="recent-grid">
#                 <div class="loading">Loading recent ads...</div>
#             </div>
#         </div>
#
#         <div class="filters">
#             <div class="filter-group">
#                 <label>🔍 Search:</label>
#                 <input type="text" id="searchInput" placeholder="Title, location, seller..." style="width: 180px;">
#             </div>
#             <div class="filter-group">
#                 <label>💰 Price:</label>
#                 <select id="priceFilter">
#                     <option value="all">All</option>
#                     <option value="crore">> 1 Crore</option>
#                     <option value="lac">< 1 Crore</option>
#                 </select>
#             </div>
#             <div class="filter-group">
#                 <label>🛋️ Furnished:</label>
#                 <select id="furnishedFilter">
#                     <option value="all">All</option>
#                     <option value="Furnished">Furnished</option>
#                     <option value="Unfurnished">Unfurnished</option>
#                 </select>
#             </div>
#             <div class="filter-group">
#                 <label>📊 Per page:</label>
#                 <select id="perPage">
#                     <option value="12">12</option>
#                     <option value="24">24</option>
#                     <option value="48">48</option>
#                 </select>
#             </div>
#             <button onclick="loadLeads()">🔄 Refresh</button>
#             <button onclick="exportCSV()">📥 Export CSV</button>
#         </div>
#
#         <div id="leadsContainer">
#             <div class="loading">Loading leads...</div>
#         </div>
#
#         <div id="pagination" class="pagination"></div>
#
#         <div class="footer">
#             Real Estate Lead Engine | Updated: <span id="timestamp"></span>
#         </div>
#     </div>
#
#     <script>
#         let currentPage = 1;
#         let totalPages = 1;
#         let allLeads = [];
#
#         // Helper to parse "X days ago", "X hours ago", "X minutes ago"
#         function parseRelativeTime(timeStr) {
#             if (!timeStr) return 999;
#             const match = timeStr.match(/(\\d+)\\s*(day|hour|minute|week|month)/i);
#             if (match) {
#                 const value = parseInt(match[1]);
#                 const unit = match[2].toLowerCase();
#                 if (unit === 'minute') return value;
#                 if (unit === 'hour') return value * 60;
#                 if (unit === 'day') return value * 1440;
#                 if (unit === 'week') return value * 10080;
#                 if (unit === 'month') return value * 43200;
#             }
#             return 999;
#         }
#
#         async function loadLeads() {
#             const search = document.getElementById('searchInput').value;
#             const price = document.getElementById('priceFilter').value;
#             const furnished = document.getElementById('furnishedFilter').value;
#             const perPage = parseInt(document.getElementById('perPage').value);
#
#             const response = await fetch(`/api/leads?search=${encodeURIComponent(search)}&price=${price}&furnished=${furnished}&page=${currentPage}&per_page=${perPage}`);
#             const data = await response.json();
#
#             allLeads = data.leads;
#             totalPages = data.total_pages;
#             currentPage = data.page;
#
#             renderLeads();
#             renderPagination();
#             updateStats(data.stats);
#
#             // Load recent ads
#             loadRecentAds();
#         }
#
#         async function loadRecentAds() {
#             const response = await fetch('/api/recent');
#             const data = await response.json();
#             renderRecentAds(data.recent);
#         }
#
#         function renderRecentAds(recent) {
#             const container = document.getElementById('recentAds');
#             if (!recent || recent.length === 0) {
#                 container.innerHTML = '<div class="no-results">No recent ads</div>';
#                 return;
#             }
#
#             let html = '';
#             for (const ad of recent.slice(0, 6)) {
#                 const title = ad.Title || 'N/A';
#                 const price = ad.Price || 'N/A';
#                 const phone = ad.Phone || 'N/A';
#                 const posted = ad.Posted || 'Unknown';
#
#                 let timeClass = '';
#                 let timeIcon = '🕐';
#                 if (posted.includes('minute')) {
#                     timeClass = 'badge-new';
#                     timeIcon = '🆕';
#                 } else if (posted.includes('hour')) {
#                     timeClass = 'badge-furnished';
#                     timeIcon = '⏰';
#                 }
#
#                 html += `
#                     <div class="recent-item">
#                         <div class="recent-icon">${timeIcon}</div>
#                         <div class="recent-info">
#                             <div class="title">${escapeHtml(title.substring(0, 50))}</div>
#                             <div class="price">💰 ${escapeHtml(price)}</div>
#                             <div class="phone">📞 ${escapeHtml(phone)}</div>
#                         </div>
#                         <div class="recent-time">
#                             <span class="time-badge ${timeClass}">${escapeHtml(posted)}</span>
#                         </div>
#                     </div>
#                 `;
#             }
#             container.innerHTML = html;
#         }
#
#         function renderLeads() {
#             const container = document.getElementById('leadsContainer');
#
#             if (allLeads.length === 0) {
#                 container.innerHTML = '<div class="no-results">No leads found. Run the pipeline first.</div>';
#                 return;
#             }
#
#             let html = '<div class="leads-grid">';
#             for (const lead of allLeads) {
#                 const title = lead.Title || 'N/A';
#                 const price = lead.Price || 'N/A';
#                 const phone = lead.Phone || 'N/A';
#                 const location = lead.Location || 'N/A';
#                 const seller = lead.Seller || 'N/A';
#                 const furnished = lead.Furnished || '';
#                 const posted = lead.Posted || 'Unknown';
#                 const image = lead.ImageURL || '';
#                 const link = lead.Link || '#';
#
#                 const furnishedBadge = furnished === 'Furnished' ? '<span class="badge badge-furnished">Furnished</span>' :
#                                       (furnished === 'Unfurnished' ? '<span class="badge badge-unfurnished">Unfurnished</span>' : '');
#
#                 // Add "New" badge for very recent ads
#                 const newBadge = (posted.includes('minute') || posted.includes('hour')) ? '<span class="badge badge-new">🆕 NEW</span>' : '';
#
#                 html += `
#                     <div class="lead-card">
#                         <div class="lead-image">
#                             ${image ? `<img src="${image}" alt="Property" loading="lazy" onerror="this.src='https://via.placeholder.com/280x160?text=No+Image'">` : '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#999;">📷 No Image</div>'}
#                         </div>
#                         <div class="lead-info">
#                             <div class="lead-title">${escapeHtml(title.substring(0, 70))}</div>
#                             <div class="lead-price">💰 ${escapeHtml(price)}</div>
#                             <div class="lead-phone">📞 ${escapeHtml(phone)}</div>
#                             <div class="lead-location">📍 ${escapeHtml(location)}</div>
#                             <div class="lead-seller">👤 ${escapeHtml(seller)} ${furnishedBadge}</div>
#                             <div class="lead-posted">
#                                 <span>📅 ${escapeHtml(posted)}</span>
#                                 ${newBadge}
#                             </div>
#                             <div class="lead-link">🔗 <a href="${link}" target="_blank">View on OLX</a></div>
#                         </div>
#                     </div>
#                 `;
#             }
#             html += '</div>';
#             container.innerHTML = html;
#         }
#
#         function renderPagination() {
#             const container = document.getElementById('pagination');
#             if (totalPages <= 1) {
#                 container.innerHTML = '';
#                 return;
#             }
#
#             let html = '';
#             for (let i = 1; i <= Math.min(totalPages, 10); i++) {
#                 html += `<button class="page-btn ${i === currentPage ? 'active' : ''}" onclick="goToPage(${i})">${i}</button>`;
#             }
#             if (totalPages > 10) {
#                 html += `<span style="padding: 6px;">...</span>`;
#                 html += `<button class="page-btn" onclick="goToPage(${totalPages})">${totalPages}</button>`;
#             }
#             container.innerHTML = html;
#         }
#
#         function goToPage(page) {
#             currentPage = page;
#             loadLeads();
#         }
#
#         function updateStats(stats) {
#             const statDivs = document.querySelectorAll('.stats-grid .stat-card');
#             if (statDivs.length >= 5) {
#                 statDivs[0].querySelector('.stat-number').textContent = stats.total_leads || 0;
#                 statDivs[1].querySelector('.stat-number').textContent = stats.with_phone || 0;
#                 statDivs[2].querySelector('.stat-number').textContent = stats.unique_locations || 0;
#                 statDivs[3].querySelector('.stat-number').textContent = stats.furnished || 0;
#                 statDivs[4].querySelector('.stat-number').textContent = stats.recent_count || 0;
#             }
#         }
#
#         function exportCSV() {
#             window.location.href = '/export/csv';
#         }
#
#         function escapeHtml(text) {
#             if (!text) return '';
#             const div = document.createElement('div');
#             div.textContent = text;
#             return div.innerHTML;
#         }
#
#         // Set timestamp
#         document.getElementById('timestamp').textContent = new Date().toLocaleString();
#
#         // Load initial data
#         loadLeads();
#
#         // Debounced search
#         let searchTimeout;
#         document.getElementById('searchInput').addEventListener('input', function() {
#             clearTimeout(searchTimeout);
#             searchTimeout = setTimeout(() => {
#                 currentPage = 1;
#                 loadLeads();
#             }, 300);
#         });
#
#         document.getElementById('priceFilter').addEventListener('change', () => { currentPage = 1; loadLeads(); });
#         document.getElementById('furnishedFilter').addEventListener('change', () => { currentPage = 1; loadLeads(); });
#         document.getElementById('perPage').addEventListener('change', () => { currentPage = 1; loadLeads(); });
#     </script>
# </body>
# </html>
# """
#
#
# def load_leads_data():
#     """Load leads from CSV file."""
#     leads_file = "data/final_leads.csv"
#     if os.path.exists(leads_file):
#         df = pd.read_csv(leads_file)
#         df = df.fillna('')
#         return df
#     return pd.DataFrame()
#
#
# def parse_time_value(time_str):
#     """Convert relative time string to minutes for sorting."""
#     if not time_str:
#         return 999999
#     time_str = str(time_str).lower()
#     match = re.search(r'(\d+)\s*(minute|hour|day|week|month)', time_str)
#     if match:
#         value = int(match.group(1))
#         unit = match.group(2)
#         if unit == 'minute':
#             return value
#         elif unit == 'hour':
#             return value * 60
#         elif unit == 'day':
#             return value * 1440
#         elif unit == 'week':
#             return value * 10080
#         elif unit == 'month':
#             return value * 43200
#     return 999999
#
#
# @app.route('/')
# def index():
#     return render_template_string(HTML_TEMPLATE)
#
#
# @app.route('/api/leads')
# def api_leads():
#     """API endpoint for leads with pagination and filters."""
#     df = load_leads_data()
#
#     if df.empty:
#         return jsonify({
#             'leads': [],
#             'total': 0,
#             'page': 1,
#             'total_pages': 1,
#             'stats': {
#                 'total_leads': 0,
#                 'with_phone': 0,
#                 'unique_locations': 0,
#                 'furnished': 0,
#                 'recent_count': 0
#             }
#         })
#
#     # Apply filters
#     search = request.args.get('search', '').lower()
#     price_filter = request.args.get('price', 'all')
#     furnished_filter = request.args.get('furnished', 'all')
#
#     if search:
#         df = df[
#             df['Title'].str.lower().str.contains(search, na=False) |
#             df['Location'].str.lower().str.contains(search, na=False) |
#             df['Seller'].str.lower().str.contains(search, na=False)
#             ]
#
#     if price_filter == 'crore':
#         df = df[df['Price'].astype(str).str.contains('Crore', na=False)]
#     elif price_filter == 'lac':
#         df = df[df['Price'].astype(str).str.contains('Lac', na=False)]
#
#     if furnished_filter != 'all':
#         df = df[df['Furnished'] == furnished_filter]
#
#     # Calculate recent count (last 24 hours)
#     recent_count = 0
#     if 'Posted' in df.columns:
#         for posted in df['Posted']:
#             if posted and ('hour' in str(posted).lower() or 'minute' in str(posted).lower()):
#                 recent_count += 1
#
#     # Calculate stats
#     stats = {
#         'total_leads': len(df),
#         'with_phone': len(df[df['Phone'].notna() & (df['Phone'] != '')]),
#         'unique_locations': df['Location'].nunique(),
#         'furnished': len(df[df['Furnished'] == 'Furnished']),
#         'recent_count': recent_count
#     }
#
#     # Pagination
#     per_page = int(request.args.get('per_page', 12))
#     page = int(request.args.get('page', 1))
#     total = len(df)
#     total_pages = (total + per_page - 1) // per_page if total > 0 else 1
#
#     start = (page - 1) * per_page
#     end = start + per_page
#
#     leads = df.iloc[start:end].to_dict('records')
#
#     return jsonify({
#         'leads': leads,
#         'total': total,
#         'page': page,
#         'total_pages': total_pages,
#         'stats': stats
#     })
#
#
# @app.route('/api/recent')
# def api_recent():
#     """API endpoint for recent ads (sorted by posting time)."""
#     df = load_leads_data()
#
#     if df.empty or 'Posted' not in df.columns:
#         return jsonify({'recent': []})
#
#     # Sort by posting time (minutes ago, ascending = more recent)
#     df_copy = df.copy()
#     df_copy['time_value'] = df_copy['Posted'].apply(parse_time_value)
#     recent_df = df_copy.sort_values('time_value').head(12)
#
#     return jsonify({'recent': recent_df.to_dict('records')})
#
#
# @app.route('/export/csv')
# def export_csv():
#     """Export leads as CSV."""
#     df = load_leads_data()
#     if df.empty:
#         return "No data to export", 404
#
#     csv_data = df.to_csv(index=False)
#     from flask import Response
#     return Response(
#         csv_data,
#         mimetype="text/csv",
#         headers={"Content-disposition": f"attachment; filename=leads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"}
#     )
#
#
# if __name__ == '__main__':
#     print("\n" + "=" * 50)
#     print("🚀 Real Estate Lead Engine Dashboard")
#     print("=" * 50)
#     print("\n📍 Dashboard URL: http://127.0.0.1:5000")
#     print("   Press Ctrl+C to stop\n")
#     app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)