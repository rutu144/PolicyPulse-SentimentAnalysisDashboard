// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function () {
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl, {
        boundary: document.body
    }));

    // Show loading spinner on form submit
    document.querySelector('form').addEventListener('submit', () => {
        document.getElementById('loading').classList.remove('d-none');
    });

    // Validate date range
    const dateStart = document.getElementById('date_start');
    const dateEnd = document.getElementById('date_end');
    
    if (dateStart && dateEnd) {
        dateStart.addEventListener('change', () => {
            if (dateStart.value) {
                dateEnd.min = dateStart.value;
            }
        });
        
        dateEnd.addEventListener('change', () => {
            if (dateEnd.value) {
                dateStart.max = dateEnd.value;
            }
        });
    }

    // Add shadow effect on scroll for navbar
    const topNav = document.querySelector('.top-nav');
    
    if (topNav) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 10) {
                topNav.style.boxShadow = '0 4px 12px rgba(0, 0, 0, 0.08)';
            } else {
                topNav.style.boxShadow = '0 2px 4px rgba(0, 0, 0, 0.08)';
            }
        });
    }

    // Add hover effects for tables
    const tableRows = document.querySelectorAll('.table tbody tr');
    
    tableRows.forEach(row => {
        row.addEventListener('mouseenter', () => {
            row.style.backgroundColor = 'rgba(67, 97, 238, 0.05)';
        });
        
        row.addEventListener('mouseleave', () => {
            row.style.backgroundColor = '';
        });
    });

    // Add animation for stat cards
    const statCards = document.querySelectorAll('.stat-card');
    let delay = 0;
    
    statCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, 100 + delay);
        
        delay += 100;
    });

    // Mobile sidebar toggle functionality
    const sidebarToggleBtn = document.createElement('button');
    sidebarToggleBtn.className = 'btn btn-primary sidebar-toggle-btn';
    sidebarToggleBtn.innerHTML = '<i class="fas fa-bars"></i>';
    sidebarToggleBtn.style.position = 'fixed';
    sidebarToggleBtn.style.top = '10px';
    sidebarToggleBtn.style.left = '10px';
    sidebarToggleBtn.style.zIndex = '1001';
    sidebarToggleBtn.style.display = 'none';
    document.body.appendChild(sidebarToggleBtn);

    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('.content');
    const footer = document.querySelector('.footer');

    function checkWindowSize() {
        if (window.innerWidth <= 768) {
            sidebarToggleBtn.style.display = 'block';
            sidebar.style.transform = 'translateX(-100%)';
            content.style.marginLeft = '0';
            footer.style.width = '100%';
        } else {
            sidebarToggleBtn.style.display = 'none';
            sidebar.style.transform = 'translateX(0)';
            content.style.marginLeft = window.innerWidth <= 992 ? '200px' : '250px';
            footer.style.width = window.innerWidth <= 992 ? 'calc(100% - 200px)' : 'calc(100% - 250px)';
        }
    }

    // Call on load and resize
    checkWindowSize();
    window.addEventListener('resize', checkWindowSize);

    // Toggle sidebar on mobile
    sidebarToggleBtn.addEventListener('click', () => {
        if (sidebar.style.transform === 'translateX(0px)') {
            sidebar.style.transform = 'translateX(-100%)';
        } else {
            sidebar.style.transform = 'translateX(0)';
        }
    });

    // Close sidebar when clicking outside on mobile
    document.addEventListener('click', (e) => {
        if (window.innerWidth <= 768 && 
            !sidebar.contains(e.target) && 
            e.target !== sidebarToggleBtn && 
            !sidebarToggleBtn.contains(e.target) && 
            sidebar.style.transform === 'translateX(0px)') {
            sidebar.style.transform = 'translateX(-100%)';
        }
    });
});