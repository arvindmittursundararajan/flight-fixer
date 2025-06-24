// DelayDeck IROPS - Application JavaScript

// Global app configuration
const DelayDeckApp = {
    config: {
        refreshInterval: 30000, // 30 seconds
        apiBaseUrl: '/api',
        autoRefresh: true,
        maxRetries: 3
    },
    
    // Initialize the application
    init: function() {
        console.log('DelayDeck IROPS Application Started');
        this.setupEventListeners();
        this.startAutoRefresh();
        this.initializeFeatherIcons();
    },
    
    // Setup global event listeners
    setupEventListeners: function() {
        // Global error handler
        window.addEventListener('error', function(e) {
            console.error('Application Error:', e.error);
        });
        
        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', function(e) {
            console.error('Unhandled Promise Rejection:', e.reason);
        });
        
        // Setup tooltips if needed
        this.initializeTooltips();
    },
    
    // Initialize Feather icons with robust error handling
    initializeFeatherIcons: function() {
        try {
            // Check if feather is available and properly loaded
            if (typeof feather !== 'undefined' && feather && typeof feather.replace === 'function') {
                feather.replace();
                console.log('Feather Icons initialized successfully');
            } else if (window.feather && typeof window.feather.replace === 'function') {
                window.feather.replace();
                console.log('Feather Icons initialized via window.feather');
            } else {
                console.warn('Feather Icons library not available - using fallback');
                this.fallbackIconInitialization();
            }
        } catch (error) {
            console.warn('Feather Icons initialization failed:', error);
            this.fallbackIconInitialization();
        }
    },
    
    // Fallback icon initialization
    fallbackIconInitialization: function() {
        try {
            // Replace feather icons with simple text or CSS icons
            const featherIcons = document.querySelectorAll('[data-feather]');
            featherIcons.forEach(icon => {
                const iconName = icon.getAttribute('data-feather');
                if (iconName) {
                    // Create a simple fallback icon using CSS or text
                    icon.innerHTML = `<span class="icon-fallback">${iconName.charAt(0).toUpperCase()}</span>`;
                    icon.classList.add('icon-fallback-container');
                }
            });
        } catch (error) {
            console.warn('Fallback icon initialization failed:', error);
        }
    },
    
    // Initialize Bootstrap tooltips
    initializeTooltips: function() {
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
            tooltipTriggerList.map(function (tooltipTriggerEl) {
                return new bootstrap.Tooltip(tooltipTriggerEl);
            });
        }
    },
    
    // Auto-refresh functionality
    startAutoRefresh: function() {
        if (this.config.autoRefresh) {
            setInterval(() => {
                this.refreshSystemStatus();
            }, this.config.refreshInterval);
        }
    },
    
    // Refresh system status
    refreshSystemStatus: function() {
        fetch(`${this.config.apiBaseUrl}/agent_status`)
            .then(response => response.json())
            .then(data => {
                this.updateSystemStatus(data);
            })
            .catch(error => {
                console.warn('Status refresh failed:', error);
                this.updateSystemStatus(null);
            });
    },
    
    // Update system status indicator
    updateSystemStatus: function(data) {
        const statusElement = document.getElementById('system-status');
        const updateTimeElement = document.getElementById('update-time');
        
        if (statusElement) {
            if (data && Object.keys(data).length > 0) {
                statusElement.className = 'badge bg-success me-2';
                statusElement.innerHTML = '<i data-feather="wifi" class="me-1"></i>System Online';
            } else {
                statusElement.className = 'badge bg-warning me-2';
                statusElement.innerHTML = '<i data-feather="wifi-off" class="me-1"></i>Limited Connectivity';
            }
            // Re-initialize icons after DOM update
            setTimeout(() => this.initializeFeatherIcons(), 100);
        }
        
        if (updateTimeElement) {
            const now = new Date();
            updateTimeElement.textContent = now.toLocaleTimeString();
        }
    },
    
    // Utility function for API calls
    apiCall: function(endpoint, options = {}) {
        const defaultOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        const finalOptions = { ...defaultOptions, ...options };
        
        return fetch(`${this.config.apiBaseUrl}${endpoint}`, finalOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            });
    },
    
    // Show loading state for buttons
    showButtonLoading: function(button, loadingText = 'Loading...') {
        if (button) {
            button.dataset.originalText = button.innerHTML;
            button.innerHTML = `<i data-feather="loader" class="me-1"></i>${loadingText}`;
            button.disabled = true;
            this.initializeFeatherIcons();
        }
    },
    
    // Hide loading state for buttons
    hideButtonLoading: function(button) {
        if (button && button.dataset.originalText) {
            button.innerHTML = button.dataset.originalText;
            button.disabled = false;
            delete button.dataset.originalText;
            this.initializeFeatherIcons();
        }
    },
    
    // Show notifications
    showNotification: function(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        // Add to page
        document.body.appendChild(notification);
        
        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
    },
    
    // Format time ago
    timeAgo: function(date) {
        const now = new Date();
        const diffInSeconds = Math.floor((now - new Date(date)) / 1000);
        
        if (diffInSeconds < 60) return 'Just now';
        if (diffInSeconds < 3600) return `${Math.floor(diffInSeconds / 60)} minutes ago`;
        if (diffInSeconds < 86400) return `${Math.floor(diffInSeconds / 3600)} hours ago`;
        return `${Math.floor(diffInSeconds / 86400)} days ago`;
    }
};

// Dashboard specific functions
const Dashboard = {
    // Refresh dashboard data
    refresh: function() {
        location.reload();
    },
    
    // Coordinate disruption
    coordinateDisruption: function(disruptionId, buttonElement) {
        if (buttonElement) {
            DelayDeckApp.showButtonLoading(buttonElement, 'Coordinating...');
        }
        
        DelayDeckApp.apiCall(`/coordinate/${disruptionId}`, {
            method: 'POST'
        })
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('Disruption coordination initiated successfully!', 'success');
                setTimeout(() => location.reload(), 2000);
            } else {
                DelayDeckApp.showNotification(`Coordination failed: ${data.error || 'Unknown error'}`, 'danger');
            }
        })
        .catch(error => {
            DelayDeckApp.showNotification(`Error: ${error.message}`, 'danger');
        })
        .finally(() => {
            if (buttonElement) {
                DelayDeckApp.hideButtonLoading(buttonElement);
            }
        });
    },
    
    // View flight details
    viewFlightDetails: function(flightId) {
        // This function is implemented in the dashboard template
        // The template function will handle the modal display
        console.log('viewFlightDetails called for flight:', flightId);
    },
    
    // Analyze delay
    analyzeDelay: function(flightId) {
        // This function is implemented in the dashboard template
        // The template function will handle the modal display
        console.log('analyzeDelay called for flight:', flightId);
    },
    
    // Show flight tab
    showFlightTab: function(tabName, buttonElement) {
        // This function is implemented in the dashboard template
        // The template function will handle tab switching
        console.log('showFlightTab called for tab:', tabName);
    }
};

// Agents page specific functions
const Agents = {
    // Refresh agent data
    refreshData: function() {
        location.reload();
    },
    
    // Switch communication view
    switchView: function(viewType, buttonElement) {
        // Update button states
        const buttonGroup = buttonElement.closest('.btn-group');
        if (buttonGroup) {
            buttonGroup.querySelectorAll('.btn').forEach(btn => {
                btn.classList.remove('active');
            });
            buttonElement.classList.add('active');
        }
        
        // Show/hide views
        const networkView = document.getElementById('network-view');
        const timelineView = document.getElementById('timeline-view');
        
        if (networkView && timelineView) {
            networkView.classList.toggle('d-none', viewType !== 'network');
            timelineView.classList.toggle('d-none', viewType !== 'timeline');
        }
    },
    
    // Filter communications
    filterCommunications: function() {
        const filter = document.getElementById('filter-agent').value;
        const rows = document.querySelectorAll('#communications-table tbody tr');
        
        rows.forEach(row => {
            if (!filter) {
                row.style.display = '';
            } else {
                const sender = row.cells[1].textContent;
                const receiver = row.cells[2].textContent;
                row.style.display = (sender.includes(filter) || receiver.includes(filter)) ? '' : 'none';
            }
        });
    },
    
    // Start all agents
    startAllAgents: function() {
        DelayDeckApp.showNotification('Starting all agents...', 'info');
        
        fetch('/api/start_agents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('All agents started successfully!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                DelayDeckApp.showNotification('Failed to start agents: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            console.error('Error starting agents:', error);
            DelayDeckApp.showNotification('Error starting agents. Please try again.', 'error');
        });
    },
    
    // Pause all agents
    pauseAllAgents: function() {
        DelayDeckApp.showNotification('Pausing all agents...', 'info');
        
        fetch('/api/pause_agents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('All agents paused successfully!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                DelayDeckApp.showNotification('Failed to pause agents: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            console.error('Error pausing agents:', error);
            DelayDeckApp.showNotification('Error pausing agents. Please try again.', 'error');
        });
    },
    
    // Reset all agents
    resetAllAgents: function() {
        if (!confirm('Are you sure you want to reset all agents? This will clear all current tasks.')) {
            return;
        }
        
        DelayDeckApp.showNotification('Resetting all agents...', 'info');
        
        fetch('/api/reset_agents', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('All agents reset successfully!', 'success');
                setTimeout(() => {
                    window.location.reload();
                }, 1500);
            } else {
                DelayDeckApp.showNotification('Failed to reset agents: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            console.error('Error resetting agents:', error);
            DelayDeckApp.showNotification('Error resetting agents. Please try again.', 'error');
        });
    },
    
    // Save agent configuration
    saveAgentConfiguration: function(agentName) {
        // Collect configuration values
        const config = {
            agent_name: agentName,
            performance: {
                response_time_limit: parseInt(document.getElementById('response-time-limit')?.value || 30),
                max_concurrent_tasks: parseInt(document.getElementById('max-tasks')?.value || 5),
                confidence_threshold: parseFloat(document.getElementById('confidence-threshold')?.value || 0.8)
            },
            communication: {
                auto_coordination: document.getElementById('auto-coordination')?.checked || false,
                real_time_updates: document.getElementById('real-time-updates')?.checked || false,
                ai_assistance: document.getElementById('ai-assistance')?.checked || false,
                notification_level: document.getElementById('notification-level')?.value || 'medium'
            },
            optimization: {
                cost_weight: parseFloat(document.getElementById('cost-weight')?.value || 0.7),
                time_weight: parseFloat(document.getElementById('time-weight')?.value || 0.8),
                quality_weight: parseFloat(document.getElementById('quality-weight')?.value || 0.9)
            }
        };
        
        // Save configuration via API
        fetch('/api/agent_config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(config)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Close the configuration modal
                const configModal = bootstrap.Modal.getInstance(document.getElementById('agentConfigOptionsModal'));
                if (configModal) {
                    configModal.hide();
                }
                
                // Show success message
                DelayDeckApp.showNotification(`${agentName} configuration saved successfully!`, 'success');
                
                // Update the agent info in the main modal
                this.updateAgentInfoWithConfig(agentName, config);
            } else {
                DelayDeckApp.showNotification('Failed to save configuration: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            console.error('Error saving agent configuration:', error);
            DelayDeckApp.showNotification('Error saving configuration. Please try again.', 'error');
        });
    },
    
    // Update agent info with configuration
    updateAgentInfoWithConfig: function(agentName, config) {
        // Update the agent overview in the main modal
        const overviewDiv = document.getElementById('agent-overview');
        if (overviewDiv) {
            const configInfo = `
                <div class="mb-3">
                    <strong class="text-dark">Configuration Status:</strong><br>
                    <span class="badge bg-success">Updated</span>
                </div>
                <div class="mb-3">
                    <strong class="text-dark">Response Time Limit:</strong><br>
                    <small class="text-muted">${config.performance.response_time_limit} seconds</small>
                </div>
                <div class="mb-3">
                    <strong class="text-dark">AI Confidence:</strong><br>
                    <small class="text-muted">${(config.performance.confidence_threshold * 100).toFixed(0)}%</small>
                </div>
            `;
            
            // Append configuration info to existing overview
            overviewDiv.innerHTML += configInfo;
        }
    }
};

// Scenarios page specific functions
const Scenarios = {
    // Create scenario
    create: function(scenarioType) {
        const typeSelect = document.getElementById('scenario-type');
        const nameInput = document.getElementById('scenario-name');
        const descriptionInput = document.getElementById('scenario-description');
        
        if (typeSelect) typeSelect.value = scenarioType;
        if (nameInput) nameInput.value = '';
        if (descriptionInput) descriptionInput.value = '';
        
        const modal = document.getElementById('createScenarioModal');
        if (modal && typeof bootstrap !== 'undefined') {
            const bsModal = new bootstrap.Modal(modal);
            bsModal.show();
        }
    },
    
    // Submit scenario
    submit: function(buttonElement) {
        const formData = {
            scenario_type: document.getElementById('scenario-type')?.value,
            name: document.getElementById('scenario-name')?.value,
            description: document.getElementById('scenario-description')?.value,
            parameters: {
                severity: document.getElementById('scenario-severity')?.value,
                duration: parseInt(document.getElementById('scenario-duration')?.value)
            }
        };
        
        if (!formData.scenario_type || !formData.name) {
            DelayDeckApp.showNotification('Please fill in all required fields', 'warning');
            return;
        }
        
        if (buttonElement) {
            DelayDeckApp.showButtonLoading(buttonElement, 'Creating...');
        }
        
        DelayDeckApp.apiCall('/create_scenario', {
            method: 'POST',
            body: JSON.stringify(formData)
        })
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('Scenario created successfully!', 'success');
                const modal = document.getElementById('createScenarioModal');
                if (modal && typeof bootstrap !== 'undefined') {
                    bootstrap.Modal.getInstance(modal)?.hide();
                }
                setTimeout(() => location.reload(), 2000);
            } else {
                DelayDeckApp.showNotification(`Failed to create scenario: ${data.error || 'Unknown error'}`, 'danger');
            }
        })
        .catch(error => {
            DelayDeckApp.showNotification(`Error: ${error.message}`, 'danger');
        })
        .finally(() => {
            if (buttonElement) {
                DelayDeckApp.hideButtonLoading(buttonElement);
            }
        });
    },
    
    // Filter scenarios
    filter: function(filter, buttonElement) {
        // Update button states
        const buttonGroup = buttonElement.closest('.btn-group');
        if (buttonGroup) {
            buttonGroup.querySelectorAll('.btn').forEach(btn => {
                btn.classList.remove('active');
            });
            buttonElement.classList.add('active');
        }
        
        DelayDeckApp.showNotification(`Filtering scenarios by: ${filter}...`, 'info');
        
        // Filter scenarios based on type
        const scenarioCards = document.querySelectorAll('.scenario-card');
        scenarioCards.forEach(card => {
            const scenarioType = card.getAttribute('data-scenario-type');
            if (filter === 'all' || scenarioType === filter) {
                card.style.display = 'block';
            } else {
                card.style.display = 'none';
            }
        });
        
        DelayDeckApp.showNotification(`Scenarios filtered by: ${filter}`, 'success');
    },
    
    // View results
    viewResults: function(scenarioId) {
        DelayDeckApp.showNotification(`Loading results for scenario ${scenarioId}...`, 'info');
        
        fetch(`/api/scenarios/${scenarioId}/results`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Create and show results modal
                const resultsModal = document.createElement('div');
                resultsModal.className = 'modal fade';
                resultsModal.id = 'scenarioResultsModal';
                resultsModal.innerHTML = `
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Scenario Results</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <h6>Performance Metrics</h6>
                                        <ul class="list-group">
                                            <li class="list-group-item d-flex justify-content-between">
                                                <span>Response Time:</span>
                                                <span class="badge bg-success">${data.results.response_time || 'N/A'}</span>
                                            </li>
                                            <li class="list-group-item d-flex justify-content-between">
                                                <span>Success Rate:</span>
                                                <span class="badge bg-info">${data.results.success_rate || 'N/A'}%</span>
                                            </li>
                                            <li class="list-group-item d-flex justify-content-between">
                                                <span>Cost Impact:</span>
                                                <span class="badge bg-warning">$${data.results.cost_impact || 'N/A'}</span>
                                            </li>
                                        </ul>
                                    </div>
                                    <div class="col-md-6">
                                        <h6>Agent Performance</h6>
                                        <div class="table-responsive">
                                            <table class="table table-sm">
                                                <thead>
                                                    <tr>
                                                        <th>Agent</th>
                                                        <th>Status</th>
                                                        <th>Tasks</th>
                                                    </tr>
                                                </thead>
                                                <tbody>
                                                    ${Object.entries(data.results.agent_performance || {}).map(([agent, perf]) => `
                                                        <tr>
                                                            <td>${agent}</td>
                                                            <td><span class="badge bg-${perf.status === 'success' ? 'success' : 'warning'}">${perf.status}</span></td>
                                                            <td>${perf.tasks_completed || 0}</td>
                                                        </tr>
                                                    `).join('')}
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" onclick="Scenarios.exportResults(${scenarioId})">Export</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(resultsModal);
                const modal = new bootstrap.Modal(resultsModal);
                modal.show();
                
                // Clean up modal after it's hidden
                resultsModal.addEventListener('hidden.bs.modal', function() {
                    document.body.removeChild(resultsModal);
                });
                
                DelayDeckApp.showNotification('Scenario results loaded successfully!', 'success');
            } else {
                DelayDeckApp.showNotification('Failed to load results: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            console.error('Error loading scenario results:', error);
            DelayDeckApp.showNotification('Error loading scenario results. Please try again.', 'error');
        });
    },
    
    // View details
    viewDetails: function(scenarioId) {
        DelayDeckApp.showNotification(`Loading details for scenario ${scenarioId}...`, 'info');
        
        fetch(`/api/scenarios/${scenarioId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Create and show details modal
                const detailsModal = document.createElement('div');
                detailsModal.className = 'modal fade';
                detailsModal.id = 'scenarioDetailsModal';
                detailsModal.innerHTML = `
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Scenario Details</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <h6>Basic Information</h6>
                                        <table class="table table-sm">
                                            <tr><td><strong>Name:</strong></td><td>${data.scenario.name}</td></tr>
                                            <tr><td><strong>Type:</strong></td><td>${data.scenario.scenario_type}</td></tr>
                                            <tr><td><strong>Status:</strong></td><td><span class="badge bg-${data.scenario.status === 'completed' ? 'success' : 'warning'}">${data.scenario.status}</span></td></tr>
                                            <tr><td><strong>Created:</strong></td><td>${new Date(data.scenario.created_at).toLocaleString()}</td></tr>
                                        </table>
                                    </div>
                                    <div class="col-md-6">
                                        <h6>Parameters</h6>
                                        <div class="card">
                                            <div class="card-body">
                                                <pre class="mb-0">${JSON.stringify(data.scenario.parameters, null, 2)}</pre>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mt-3">
                                    <div class="col-12">
                                        <h6>Description</h6>
                                        <p>${data.scenario.description || 'No description available.'}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                <button type="button" class="btn btn-primary" onclick="Scenarios.viewResults(${scenarioId})">View Results</button>
                            </div>
                        </div>
                    </div>
                `;
                
                document.body.appendChild(detailsModal);
                const modal = new bootstrap.Modal(detailsModal);
                modal.show();
                
                // Clean up modal after it's hidden
                detailsModal.addEventListener('hidden.bs.modal', function() {
                    document.body.removeChild(detailsModal);
                });
                
                DelayDeckApp.showNotification('Scenario details loaded successfully!', 'success');
            } else {
                DelayDeckApp.showNotification('Failed to load details: ' + (data.error || 'Unknown error'), 'error');
            }
        })
        .catch(error => {
            console.error('Error loading scenario details:', error);
            DelayDeckApp.showNotification('Error loading scenario details. Please try again.', 'error');
        });
    },
    
    // Export results
    exportResults: function(scenarioId) {
        DelayDeckApp.showNotification('Exporting scenario results...', 'info');
        
        fetch(`/api/scenarios/${scenarioId}/export`)
        .then(response => response.blob())
        .then(blob => {
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `scenario_${scenarioId}_results.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
            DelayDeckApp.showNotification('Scenario results exported successfully!', 'success');
        })
        .catch(error => {
            console.error('Error exporting results:', error);
            DelayDeckApp.showNotification('Error exporting results. Please try again.', 'error');
        });
    },
    
    // Coordination Testing Functions
    
    // Run quick coordination test
    runQuickCoordinationTest: function(buttonElement) {
        if (buttonElement) {
            DelayDeckApp.showButtonLoading(buttonElement, 'Running Quick Test...');
        }
        
        DelayDeckApp.showNotification('Starting quick coordination test...', 'info');
        
        // Get available disruptions first
        fetch('/api/test/coordination/disruptions')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.disruptions && data.disruptions.length > 0) {
                const disruptionId = data.selected_id;
                return this.executeQuickTest(disruptionId, buttonElement);
            } else {
                throw new Error('No disruptions available for testing');
            }
        })
        .catch(error => {
            console.error('Error in quick coordination test:', error);
            DelayDeckApp.showNotification(`Quick test failed: ${error.message}`, 'danger');
            if (buttonElement) {
                DelayDeckApp.hideButtonLoading(buttonElement);
            }
        });
    },
    
    // Execute quick test with specific disruption
    executeQuickTest: function(disruptionId, buttonElement) {
        return fetch(`/api/test/coordination/quick/${disruptionId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('Quick coordination test completed successfully!', 'success');
                this.displayTestResults(data, 'Quick Test Results');
            } else {
                throw new Error(data.error || 'Quick test failed');
            }
        })
        .catch(error => {
            throw error;
        })
        .finally(() => {
            if (buttonElement) {
                DelayDeckApp.hideButtonLoading(buttonElement);
            }
        });
    },
    
    // Run full coordination test
    runFullCoordinationTest: function(buttonElement) {
        if (buttonElement) {
            DelayDeckApp.showButtonLoading(buttonElement, 'Running Full Test...');
        }
        
        DelayDeckApp.showNotification('Starting full coordination test...', 'info');
        
        // Get form data
        const disruptionId = document.getElementById('test-disruption-id')?.value || null;
        const waitTime = parseInt(document.getElementById('test-wait-time')?.value || 10);
        
        const testData = {
            disruption_id: disruptionId ? parseInt(disruptionId) : null,
            wait_time: waitTime
        };
        
        fetch('/api/test/coordination/full', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(testData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('Full coordination test completed successfully!', 'success');
                this.displayTestResults(data, 'Full Test Results');
            } else {
                throw new Error(data.error || 'Full test failed');
            }
        })
        .catch(error => {
            console.error('Error in full coordination test:', error);
            DelayDeckApp.showNotification(`Full test failed: ${error.message}`, 'danger');
        })
        .finally(() => {
            if (buttonElement) {
                DelayDeckApp.hideButtonLoading(buttonElement);
            }
        });
    },
    
    // Display test results in a modal
    displayTestResults: function(data, title) {
        const resultsModal = document.createElement('div');
        resultsModal.className = 'modal fade';
        resultsModal.id = 'coordinationTestResultsModal';
        
        const statusClass = data.status === 'SUCCESS' ? 'success' : 
                           data.status === 'FAILURE' ? 'danger' : 
                           data.status === 'TIMEOUT' ? 'warning' : 'info';
        
        resultsModal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row mb-3">
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h6 class="card-title">Test Summary</h6>
                                        <p class="mb-1"><strong>Status:</strong> 
                                            <span class="badge bg-${statusClass}">${data.status}</span>
                                        </p>
                                        <p class="mb-1"><strong>Duration:</strong> ${data.duration.toFixed(2)}s</p>
                                        <p class="mb-1"><strong>Message:</strong> ${data.message}</p>
                                        <p class="mb-0"><strong>Timestamp:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="card">
                                    <div class="card-body">
                                        <h6 class="card-title">Quick Actions</h6>
                                        <button class="btn btn-sm btn-outline-primary mb-2 w-100" onclick="Scenarios.exportTestResults(${JSON.stringify(data).replace(/"/g, '&quot;')})">
                                            <i data-feather="download" class="me-1"></i>Export Results
                                        </button>
                                        <button class="btn btn-sm btn-outline-secondary mb-2 w-100" onclick="Scenarios.runSystemCheck()">
                                            <i data-feather="activity" class="me-1"></i>System Check
                                        </button>
                                        <button class="btn btn-sm btn-outline-info w-100" onclick="Scenarios.viewCommunications(${data.data?.disruption_id || 'null'})">
                                            <i data-feather="message-circle" class="me-1"></i>View Communications
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                        
                        ${data.data && data.data.steps ? `
                        <div class="row">
                            <div class="col-12">
                                <h6>Detailed Results</h6>
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>Step</th>
                                                <th>Status</th>
                                                <th>Message</th>
                                                <th>Duration</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${data.data.steps.map(step => {
                                                const stepStatusClass = step.result.status === 'success' ? 'success' : 
                                                                       step.result.status === 'failure' ? 'danger' : 'warning';
                                                return `
                                                    <tr>
                                                        <td>${step.name}</td>
                                                        <td><span class="badge bg-${stepStatusClass}">${step.result.status}</span></td>
                                                        <td>${step.result.message}</td>
                                                        <td>${step.result.duration ? step.result.duration.toFixed(2) + 's' : 'N/A'}</td>
                                                    </tr>
                                                `;
                                            }).join('')}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                        ` : ''}
                        
                        ${data.error_details ? `
                        <div class="row mt-3">
                            <div class="col-12">
                                <div class="alert alert-danger">
                                    <h6>Error Details</h6>
                                    <pre class="mb-0">${data.error_details}</pre>
                                </div>
                            </div>
                        </div>
                        ` : ''}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="Scenarios.runFullCoordinationTest()">Run Another Test</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(resultsModal);
        const modal = new bootstrap.Modal(resultsModal);
        modal.show();
        
        // Initialize icons
        setTimeout(() => DelayDeckApp.initializeFeatherIcons(), 100);
        
        // Clean up modal after it's hidden
        resultsModal.addEventListener('hidden.bs.modal', function() {
            document.body.removeChild(resultsModal);
        });
    },
    
    // Export test results
    exportTestResults: function(data) {
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `coordination_test_${new Date().toISOString().slice(0, 19).replace(/:/g, '-')}.json`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        DelayDeckApp.showNotification('Test results exported successfully!', 'success');
    },
    
    // Run system check
    runSystemCheck: function() {
        DelayDeckApp.showNotification('Running system check...', 'info');
        
        fetch('/api/test/coordination/status')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                DelayDeckApp.showNotification('System check completed successfully!', 'success');
                this.displayTestResults(data, 'System Check Results');
            } else {
                throw new Error(data.error || 'System check failed');
            }
        })
        .catch(error => {
            console.error('Error in system check:', error);
            DelayDeckApp.showNotification(`System check failed: ${error.message}`, 'danger');
        });
    },
    
    // View communications for a disruption
    viewCommunications: function(disruptionId) {
        if (!disruptionId) {
            DelayDeckApp.showNotification('No disruption ID available', 'warning');
            return;
        }
        
        DelayDeckApp.showNotification(`Loading communications for disruption ${disruptionId}...`, 'info');
        
        fetch(`/api/communications/${disruptionId}`)
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                this.displayCommunications(data.communications, disruptionId);
            } else {
                throw new Error(data.error || 'Failed to load communications');
            }
        })
        .catch(error => {
            console.error('Error loading communications:', error);
            DelayDeckApp.showNotification(`Failed to load communications: ${error.message}`, 'danger');
        });
    },
    
    // Display communications in a modal
    displayCommunications: function(communications, disruptionId) {
        const commModal = document.createElement('div');
        commModal.className = 'modal fade';
        commModal.id = 'communicationsModal';
        
        commModal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Communications for Disruption ${disruptionId}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        ${communications && communications.length > 0 ? `
                        <div class="table-responsive">
                            <table class="table table-sm">
                                <thead>
                                    <tr>
                                        <th>Timestamp</th>
                                        <th>From</th>
                                        <th>To</th>
                                        <th>Type</th>
                                        <th>Message</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${communications.map(comm => `
                                        <tr>
                                            <td>${new Date(comm.timestamp).toLocaleString()}</td>
                                            <td><span class="badge bg-primary">${comm.sender}</span></td>
                                            <td><span class="badge bg-secondary">${comm.receiver}</span></td>
                                            <td><span class="badge bg-info">${comm.message_type}</span></td>
                                            <td>${comm.message}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                        ` : `
                        <div class="alert alert-info">
                            No communications found for this disruption.
                        </div>
                        `}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(commModal);
        const modal = new bootstrap.Modal(commModal);
        modal.show();
        
        // Clean up modal after it's hidden
        commModal.addEventListener('hidden.bs.modal', function() {
            document.body.removeChild(commModal);
        });
        
        DelayDeckApp.showNotification(`Communications loaded for disruption ${disruptionId}`, 'success');
    }
};

// Global function aliases for backward compatibility
window.refreshDashboard = Dashboard.refresh;

window.refreshAgentData = Agents.refreshData;
window.switchView = (view) => Agents.switchView(view, event.target);
window.filterCommunications = Agents.filterCommunications;
window.startAllAgents = Agents.startAllAgents;
window.pauseAllAgents = Agents.pauseAllAgents;
window.resetAllAgents = Agents.resetAllAgents;
window.saveAgentConfiguration = (agentName) => Agents.saveAgentConfiguration(agentName);

window.createScenario = Scenarios.create;
window.submitScenario = () => Scenarios.submit(event.target);
window.filterScenarios = (filter) => Scenarios.filter(filter, event.target);
window.viewResults = Scenarios.viewResults;
window.viewScenarioDetails = Scenarios.viewDetails;

// Coordination testing function aliases
window.runQuickCoordinationTest = (buttonElement) => Scenarios.runQuickCoordinationTest(buttonElement);
window.runFullCoordinationTest = (buttonElement) => Scenarios.runFullCoordinationTest(buttonElement);

// BEGIN: Business Metrics Tab Logic (AI ADDED)
document.addEventListener('DOMContentLoaded', function() {
    var metricsTab = document.getElementById('metrics-tab');
    if (metricsTab) {
        console.log('Business Metrics tab found, setting up event listener');
        metricsTab.addEventListener('shown.bs.tab', function (event) {
            console.log('Business Metrics tab activated');
            // Get the current disruption ID from the modal context
            var disruptionId = window.currentDisruptionId;
            console.log('Current disruption ID:', disruptionId);
            
            if (!disruptionId) {
                console.warn('No disruption ID available for Business Metrics, trying fallback...');
                // Fallback: try to get disruption ID from URL or other sources
                disruptionId = getDisruptionIdFromFallback();
                if (!disruptionId) {
                    showMetricsError('No disruption selected. Please select a disruption first.');
                    return;
                }
            }
            
            console.log('Fetching business metrics for disruption:', disruptionId);
            fetchBusinessMetrics(disruptionId);
        });
    } else {
        console.warn('Business Metrics tab not found in DOM');
    }
});

function getDisruptionIdFromFallback() {
    // Try multiple fallback methods to get disruption ID
    console.log('Attempting fallback methods to get disruption ID...');
    
    // Method 1: Check if there's an active coordination modal with disruption info
    var modal = document.getElementById('coordinationModal');
    if (modal && modal.classList.contains('show')) {
        console.log('Coordination modal is active, checking for disruption info...');
        // Look for any elements that might contain disruption ID
        var disruptionElements = modal.querySelectorAll('[data-disruption-id]');
        if (disruptionElements.length > 0) {
            var id = disruptionElements[0].getAttribute('data-disruption-id');
            console.log('Found disruption ID from modal elements:', id);
            return id;
        }
    }
    
    // Method 2: Check URL parameters
    var urlParams = new URLSearchParams(window.location.search);
    var urlDisruptionId = urlParams.get('disruption_id');
    if (urlDisruptionId) {
        console.log('Found disruption ID from URL:', urlDisruptionId);
        return urlDisruptionId;
    }
    
    // Method 3: Check localStorage or sessionStorage
    var storedId = sessionStorage.getItem('currentDisruptionId') || localStorage.getItem('currentDisruptionId');
    if (storedId) {
        console.log('Found disruption ID from storage:', storedId);
        return storedId;
    }
    
    console.log('No fallback disruption ID found');
    return null;
}

function fetchBusinessMetrics(disruptionId) {
    console.log('fetchBusinessMetrics called with disruptionId:', disruptionId);
    var spinner = document.getElementById('metrics-loading-spinner');
    var errorDiv = document.getElementById('metrics-error');
    var dataDiv = document.getElementById('metrics-data');
    
    // Show loading state
    if (spinner) {
        spinner.classList.remove('d-none');
        console.log('Showing loading spinner');
    }
    if (errorDiv) { 
        errorDiv.classList.add('d-none'); 
        errorDiv.innerHTML = ''; 
    }
    if (dataDiv) dataDiv.innerHTML = '';

    console.log('Making API call to /api/business_metrics/' + disruptionId);
    fetch(`/api/business_metrics/${disruptionId}`)
        .then(response => {
            console.log('API response status:', response.status);
            if (!response.ok) throw new Error('Failed to fetch business metrics: ' + response.status);
            return response.json();
        })
        .then(data => {
            console.log('Business metrics data received:', data);
            if (!data.success) throw new Error(data.error || 'Unknown error');
            renderBusinessMetrics(data.metrics);
        })
        .catch(err => {
            console.error('Business Metrics Fetch Error:', err);
            showMetricsError('Could not load business metrics. ' + err.message);
        })
        .finally(() => {
            if (spinner) {
                spinner.classList.add('d-none');
                console.log('Hiding loading spinner');
            }
        });
}

function showMetricsError(msg) {
    console.error('Showing metrics error:', msg);
    var errorDiv = document.getElementById('metrics-error');
    var dataDiv = document.getElementById('metrics-data');
    if (errorDiv) {
        errorDiv.textContent = msg;
        errorDiv.classList.remove('d-none');
    }
    if (dataDiv) dataDiv.innerHTML = '';
}

function renderBusinessMetrics(metrics) {
    console.log('Rendering business metrics:', metrics);
    var dataDiv = document.getElementById('metrics-data');
    if (!dataDiv) {
        console.error('Metrics data div not found');
        return;
    }
    try {
        // Beautiful, organized rendering of business metrics
        let html = `
            <div class="business-metrics-container">
                <!-- Header -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 bg-gradient-primary text-white">
                            <div class="card-body text-center">
                                <h4 class="mb-2"><i data-feather="bar-chart-2" class="me-2"></i>Business Metrics Dashboard</h4>
                                <p class="mb-0">Comprehensive analysis of coordination impact and business value</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Airline Information -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 shadow-sm">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="plane" class="me-2 text-primary"></i>Airline Operations</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <div class="d-flex align-items-center mb-3">
                                            <div class="bg-primary bg-opacity-10 p-3 rounded me-3">
                                                <i data-feather="building" class="text-primary"></i>
                                            </div>
                                            <div>
                                                <h6 class="mb-1">Airline</h6>
                                                <p class="mb-0 text-muted">${metrics.airline_info?.airline || 'Unknown'}</p>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="d-flex align-items-center mb-3">
                                            <div class="bg-success bg-opacity-10 p-3 rounded me-3">
                                                <i data-feather="activity" class="text-success"></i>
                                            </div>
                                            <div>
                                                <h6 class="mb-1">Operations Status</h6>
                                                <p class="mb-0 text-muted">${metrics.airline_info?.operations || 'No flights affected'}</p>
                                                <!-- Insert flight numbers display here -->
                                                ${(metrics.airline_info?.flight_numbers_display) ? `
                                                    <div class='mt-2 text-dark fw-bold'>${metrics.airline_info.flight_numbers_display}</div>
                                                ` : ''}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Business Impact Overview -->
                <div class="row mb-4">
                    <div class="col-12">
                        <h5 class="text-dark mb-3"><i data-feather="trending-up" class="me-2 text-success"></i>Business Impact Analysis</h5>
                    </div>
                </div>

                <!-- Customer Impact -->
                <div class="row mb-4">
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="users" class="me-2 text-info"></i>Customer Impact</h6>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-6 mb-3">
                                        <div class="bg-info bg-opacity-10 p-3 rounded">
                                            <h4 class="text-info mb-1">${metrics.business_impact?.customer_impact?.passengers_affected || 0}</h4>
                                            <small class="text-muted">Passengers Affected</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-warning bg-opacity-10 p-3 rounded">
                                            <h4 class="text-warning mb-1">${metrics.business_impact?.customer_impact?.rebooking_rate || '85%'}</h4>
                                            <small class="text-muted">Rebooking Rate</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-danger bg-opacity-10 p-3 rounded">
                                            <h4 class="text-danger mb-1">${metrics.business_impact?.customer_impact?.customer_satisfaction_impact || '-25%'}</h4>
                                            <small class="text-muted">Satisfaction Impact</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-secondary bg-opacity-10 p-3 rounded">
                                            <h4 class="text-secondary mb-1">${metrics.business_impact?.customer_impact?.loyalty_impact || '-10%'}</h4>
                                            <small class="text-muted">Loyalty Impact</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Financial Impact -->
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="dollar-sign" class="me-2 text-success"></i>Financial Impact</h6>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-6 mb-3">
                                        <div class="bg-success bg-opacity-10 p-3 rounded">
                                            <h4 class="text-success mb-1">$${metrics.business_impact?.financial_impact?.total_impact?.toLocaleString() || 0}</h4>
                                            <small class="text-muted">Total Impact</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-primary bg-opacity-10 p-3 rounded">
                                            <h4 class="text-primary mb-1">$${metrics.business_impact?.financial_impact?.compensation_cost?.toLocaleString() || 0}</h4>
                                            <small class="text-muted">Compensation Cost</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-warning bg-opacity-10 p-3 rounded">
                                            <h4 class="text-warning mb-1">$${metrics.business_impact?.financial_impact?.operational_cost_impact?.toLocaleString() || 0}</h4>
                                            <small class="text-muted">Operational Cost</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-info bg-opacity-10 p-3 rounded">
                                            <h4 class="text-info mb-1">$${metrics.business_impact?.financial_impact?.passenger_revenue_impact?.toLocaleString() || 0}</h4>
                                            <small class="text-muted">Revenue Impact</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Operational Impact -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 shadow-sm">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="settings" class="me-2 text-warning"></i>Operational Impact</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-warning bg-opacity-10 p-3 rounded">
                                            <h4 class="text-warning mb-1">${metrics.business_impact?.operational_impact?.affected_flights || 0}</h4>
                                            <small class="text-muted">Affected Flights</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-danger bg-opacity-10 p-3 rounded">
                                            <h4 class="text-danger mb-1">${metrics.business_impact?.operational_impact?.total_delay_minutes || 0}</h4>
                                            <small class="text-muted">Total Delay (min)</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-info bg-opacity-10 p-3 rounded">
                                            <h4 class="text-info mb-1">${metrics.business_impact?.operational_impact?.average_delay_per_flight || 0}</h4>
                                            <small class="text-muted">Avg Delay/Flight</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-secondary bg-opacity-10 p-3 rounded">
                                            <h4 class="text-secondary mb-1">${metrics.business_impact?.operational_impact?.total_passengers || 0}</h4>
                                            <small class="text-muted">Total Passengers</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mt-3">
                                    <div class="col-md-6">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <span>On-Time Performance Impact:</span>
                                            <span class="badge bg-warning">${metrics.business_impact?.operational_impact?.on_time_performance_impact || '-15%'}</span>
                                        </div>
                                        <div class="progress mb-3" style="height: 8px;">
                                            <div class="progress-bar bg-warning" style="width: 15%"></div>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <div class="d-flex justify-content-between align-items-center mb-2">
                                            <span>Capacity Utilization Impact:</span>
                                            <span class="badge bg-danger">${metrics.business_impact?.operational_impact?.capacity_utilization_impact || '-20%'}</span>
                                        </div>
                                        <div class="progress mb-3" style="height: 8px;">
                                            <div class="progress-bar bg-danger" style="width: 20%"></div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Coordination Effectiveness -->
                <div class="row mb-4">
                    <div class="col-12">
                        <h5 class="text-dark mb-3"><i data-feather="target" class="me-2 text-primary"></i>Coordination Effectiveness</h5>
                    </div>
                </div>

                <div class="row mb-4">
                    <!-- Agent Coordination -->
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="users" class="me-2 text-primary"></i>Agent Coordination</h6>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-6 mb-3">
                                        <div class="bg-primary bg-opacity-10 p-3 rounded">
                                            <h4 class="text-primary mb-1">${metrics.coordination_effectiveness?.agent_coordination?.agents_involved || 5}</h4>
                                            <small class="text-muted">Agents Involved</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-success bg-opacity-10 p-3 rounded">
                                            <h4 class="text-success mb-1">${metrics.coordination_effectiveness?.agent_coordination?.coordination_success_rate || '92%'}</h4>
                                            <small class="text-muted">Success Rate</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-3">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span>Dependency Management:</span>
                                        <span class="badge bg-info">${metrics.coordination_effectiveness?.agent_coordination?.dependency_management || 'Automated'}</span>
                                    </div>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span>Parallel Processing:</span>
                                        <span class="badge bg-success">${metrics.coordination_effectiveness?.agent_coordination?.parallel_processing || 'Enabled'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Communication Metrics -->
                    <div class="col-md-6">
                        <div class="card border-0 shadow-sm h-100">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="message-circle" class="me-2 text-info"></i>Communication Metrics</h6>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-6 mb-3">
                                        <div class="bg-info bg-opacity-10 p-3 rounded">
                                            <h4 class="text-info mb-1">${metrics.coordination_effectiveness?.communication_metrics?.total_messages || 47}</h4>
                                            <small class="text-muted">Total Messages</small>
                                        </div>
                                    </div>
                                    <div class="col-6 mb-3">
                                        <div class="bg-warning bg-opacity-10 p-3 rounded">
                                            <h4 class="text-warning mb-1">${metrics.coordination_effectiveness?.communication_metrics?.messages_per_agent || 9.4}</h4>
                                            <small class="text-muted">Messages/Agent</small>
                                        </div>
                                    </div>
                                </div>
                                <div class="mt-3">
                                    <div class="d-flex justify-content-between align-items-center mb-2">
                                        <span>Information Accuracy:</span>
                                        <span class="badge bg-success">${metrics.coordination_effectiveness?.communication_metrics?.information_accuracy || '95%'}</span>
                                    </div>
                                    <div class="d-flex justify-content-between align-items-center">
                                        <span>Response Times:</span>
                                        <span class="badge bg-primary">${metrics.coordination_effectiveness?.communication_metrics?.response_times || 'Under 30 seconds'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Cost Analysis -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 shadow-sm">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="dollar-sign" class="me-2 text-success"></i>Cost Analysis</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-6">
                                        <h6 class="text-success mb-3">Coordinated Approach</h6>
                                        <div class="table-responsive">
                                            <table class="table table-sm">
                                                <tbody>
                                                    <tr>
                                                        <td>Coordination System Cost:</td>
                                                        <td class="text-end">$${metrics.cost_analysis?.coordinated_approach?.coordination_system_cost?.toLocaleString() || 5000}</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Passenger Compensation:</td>
                                                        <td class="text-end">$${metrics.cost_analysis?.coordinated_approach?.passenger_compensation?.toLocaleString() || 0}</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Operational Inefficiencies:</td>
                                                        <td class="text-end">$${metrics.cost_analysis?.coordinated_approach?.operational_inefficiencies?.toLocaleString() || 0}</td>
                                                    </tr>
                                                    <tr class="table-success">
                                                        <td><strong>Total Coordinated Cost:</strong></td>
                                                        <td class="text-end"><strong>$${metrics.cost_analysis?.coordinated_approach?.total?.toLocaleString() || 5000}</strong></td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                    <div class="col-md-6">
                                        <h6 class="text-danger mb-3">Traditional Approach</h6>
                                        <div class="table-responsive">
                                            <table class="table table-sm">
                                                <tbody>
                                                    <tr>
                                                        <td>Passenger Compensation:</td>
                                                        <td class="text-end">$${metrics.cost_analysis?.traditional_approach?.passenger_compensation?.toLocaleString() || 0}</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Operational Inefficiencies:</td>
                                                        <td class="text-end">$${metrics.cost_analysis?.traditional_approach?.operational_inefficiencies?.toLocaleString() || 0}</td>
                                                    </tr>
                                                    <tr>
                                                        <td>Regulatory Penalties:</td>
                                                        <td class="text-end">$${metrics.cost_analysis?.traditional_approach?.regulatory_penalties?.toLocaleString() || 0}</td>
                                                    </tr>
                                                    <tr class="table-danger">
                                                        <td><strong>Total Traditional Cost:</strong></td>
                                                        <td class="text-end"><strong>$${metrics.cost_analysis?.traditional_approach?.total?.toLocaleString() || 0}</strong></td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </div>
                                    </div>
                                </div>
                                <div class="row mt-3">
                                    <div class="col-12">
                                        <div class="alert alert-info">
                                            <div class="d-flex justify-content-between align-items-center">
                                                <div>
                                                    <h6 class="mb-1"><i data-feather="trending-up" class="me-2"></i>Cost Savings Analysis</h6>
                                                    <p class="mb-0">Total savings: <strong>$${metrics.cost_analysis?.savings?.total_savings?.toLocaleString() || -5000}</strong> | ROI: <strong>${metrics.cost_analysis?.savings?.roi || -100}%</strong></p>
                                                </div>
                                                <div class="text-end">
                                                    <span class="badge bg-${metrics.cost_analysis?.savings?.roi > 0 ? 'success' : 'danger'} fs-6">
                                                        ${metrics.cost_analysis?.savings?.roi > 0 ? 'Positive' : 'Negative'} ROI
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Reputation Impact -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 shadow-sm">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="star" class="me-2 text-warning"></i>Reputation Impact</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-warning bg-opacity-10 p-3 rounded">
                                            <h4 class="text-warning mb-1">${metrics.business_impact?.reputation_impact?.brand_impact || 'Moderate'}</h4>
                                            <small class="text-muted">Brand Impact</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-danger bg-opacity-10 p-3 rounded">
                                            <h4 class="text-danger mb-1">${metrics.business_impact?.reputation_impact?.negative_sentiment || '35%'}</h4>
                                            <small class="text-muted">Negative Sentiment</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-info bg-opacity-10 p-3 rounded">
                                            <h4 class="text-info mb-1">${metrics.business_impact?.reputation_impact?.recovery_time || '48-72 hours'}</h4>
                                            <small class="text-muted">Recovery Time</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-secondary bg-opacity-10 p-3 rounded">
                                            <h4 class="text-secondary mb-1">${metrics.business_impact?.reputation_impact?.social_media_mentions || 0}</h4>
                                            <small class="text-muted">Social Mentions</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- System Performance -->
                <div class="row mb-4">
                    <div class="col-12">
                        <div class="card border-0 shadow-sm">
                            <div class="card-header bg-light">
                                <h6 class="mb-0"><i data-feather="cpu" class="me-2 text-info"></i>System Performance</h6>
                            </div>
                            <div class="card-body">
                                <div class="row">
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-success bg-opacity-10 p-3 rounded">
                                            <h4 class="text-success mb-1">${metrics.coordination_effectiveness?.system_performance?.reliability || '99.5%'}</h4>
                                            <small class="text-muted">Reliability</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-primary bg-opacity-10 p-3 rounded">
                                            <h4 class="text-primary mb-1">${metrics.coordination_effectiveness?.system_performance?.response_time || 'Under 5 seconds'}</h4>
                                            <small class="text-muted">Response Time</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-warning bg-opacity-10 p-3 rounded">
                                            <h4 class="text-warning mb-1">${metrics.coordination_effectiveness?.system_performance?.scalability || 'High'}</h4>
                                            <small class="text-muted">Scalability</small>
                                        </div>
                                    </div>
                                    <div class="col-md-3 text-center mb-3">
                                        <div class="bg-info bg-opacity-10 p-3 rounded">
                                            <h4 class="text-info mb-1">${metrics.coordination_effectiveness?.system_performance?.uptime || '99.9%'}</h4>
                                            <small class="text-muted">Uptime</small>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Footer -->
                <div class="row">
                    <div class="col-12">
                        <div class="card border-0 bg-light">
                            <div class="card-body text-center">
                                <p class="mb-0 text-muted">
                                    <i data-feather="clock" class="me-1"></i>
                                    Metrics generated at: ${new Date().toLocaleString()}
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        dataDiv.innerHTML = html;
        
        // Reinitialize Feather icons after rendering
        setTimeout(() => {
            if (typeof feather !== 'undefined' && feather && typeof feather.replace === 'function') {
                feather.replace();
            }
        }, 100);
        
        console.log('Business metrics rendered successfully');
    } catch (e) {
        console.error('Business Metrics Render Error:', e);
        showMetricsError('Error rendering metrics: ' + e.message);
    }
}
// END: Business Metrics Tab Logic (AI ADDED)

// Global function for resetting and reseeding database
function resetAndReseedDatabase() {
    if (!confirm('This will clear all existing data and reseed the database with realistic airline disruption scenarios. Are you sure you want to continue?')) {
        return;
    }
    
    const button = event.target.closest('button');
    if (button) {
        DelayDeckApp.showButtonLoading(button, 'Reseeding...');
    }
    
    // Show initial notification
    DelayDeckApp.showNotification('Starting database reset and reseed process...', 'info');
    
    fetch('/api/seed_realistic_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        DelayDeckApp.showNotification('Database successfully reset and reseeded! Refreshing page...', 'success');
        
        // Hide button loading
        if (button) {
            DelayDeckApp.hideButtonLoading(button);
        }
        
        // Refresh the page after a short delay to show new data
        setTimeout(() => {
            window.location.reload();
        }, 2000);
    })
    .catch(error => {
        console.error('Database reseed failed:', error);
        DelayDeckApp.showNotification('Failed to reset and reseed database. Please try again.', 'error');
        
        // Hide button loading
        if (button) {
            DelayDeckApp.hideButtonLoading(button);
        }
    });
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    DelayDeckApp.init();
});

// Export for potential module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { DelayDeckApp, Dashboard, Agents, Scenarios };
}
