document.addEventListener('DOMContentLoaded', () => {
    // 1. Preloader Dismissal (Fade-out animation)
    const preloader = document.getElementById('preloader');
    if (preloader) {
        window.addEventListener('load', () => {
            setTimeout(() => {
                preloader.style.opacity = '0';
                preloader.style.visibility = 'hidden';
            }, 600); // smooth entry
        });

        // Safety timeout
        setTimeout(() => {
            preloader.style.opacity = '0';
            preloader.style.visibility = 'hidden';
        }, 3000);
    }

    // 2. Custom Cursor removed

    // 3. Sticky Navbar & Active Section Link tracking
    const navbar = document.getElementById('navbar');
    const sections = document.querySelectorAll('section[id]');

    window.addEventListener('scroll', () => {
        // Sticky background transformation
        if (window.scrollY > 50) {
            navbar.classList.add('bg-white/95', 'backdrop-blur-md', 'shadow-sm', 'border-b', 'border-slate-100', 'py-4');
            navbar.classList.remove('bg-transparent', 'py-6');
        } else {
            navbar.classList.remove('bg-white/95', 'backdrop-blur-md', 'shadow-sm', 'border-b', 'border-slate-100', 'py-4');
            navbar.classList.add('bg-transparent', 'py-6');
        }

        // Active link tracking
        let scrollY = window.pageYOffset;
        sections.forEach(current => {
            const sectionHeight = current.offsetHeight;
            const sectionTop = current.offsetTop - 120;
            const sectionId = current.getAttribute('id');

            if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
                document.querySelector(`.nav-link[href*=${sectionId}]`)?.classList.add('nav-link-active');
            } else {
                document.querySelector(`.nav-link[href*=${sectionId}]`)?.classList.remove('nav-link-active');
            }
        });
    });

    // 4. Mobile Hamburger Menu Toggle with slide height transition
    const mobileMenuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuBtn && mobileMenu) {
        mobileMenuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('menu-active');
        });

        // Close mobile menu on clicking any navigation link
        const mobileLinks = mobileMenu.querySelectorAll('a');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenu.classList.remove('menu-active');
            });
        });
    }

    // 5. Scroll-to-Top Button Functionality
    const scrollTopBtn = document.getElementById('scroll-to-top');
    if (scrollTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.scrollY > 400) {
                scrollTopBtn.classList.add('show');
            } else {
                scrollTopBtn.classList.remove('show');
            }
        });

        scrollTopBtn.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // 6. Project Category Filter
    const filterButtons = document.querySelectorAll('.filter-btn');
    const projectCards = document.querySelectorAll('.project-card-item');

    filterButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            filterButtons.forEach(b => {
                b.classList.remove('bg-black', 'text-white', 'border-black');
                b.classList.add('bg-white', 'text-black', 'border-slate-200');
            });

            btn.classList.remove('bg-white', 'text-black', 'border-slate-200');
            btn.classList.add('bg-black', 'text-white', 'border-black');

            const category = btn.getAttribute('data-filter');

            projectCards.forEach(card => {
                if (category === 'all') {
                    card.style.display = 'flex'; // maintain flex grid structures
                } else {
                    const cardCategory = card.getAttribute('data-category');
                    if (cardCategory.toLowerCase() === category.toLowerCase()) {
                        card.style.display = 'flex';
                    } else {
                        card.style.display = 'none';
                    }
                }
            });
        });
    });

    // 7. Dynamic Project Preview Modal opening & scale transitions
    const modal = document.getElementById('project-modal');
    const modalClose = document.getElementById('modal-close');
    const modalTitle = document.getElementById('modal-title');
    const modalDesc = document.getElementById('modal-desc');
    const modalImage = document.getElementById('modal-image');
    const modalTech = document.getElementById('modal-tech');
    const modalGithub = document.getElementById('modal-github');
    const modalDemo = document.getElementById('modal-demo');
    const modalCategory = document.getElementById('modal-category');

    const viewProjectButtons = document.querySelectorAll('.view-project-btn');

    viewProjectButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const title = btn.getAttribute('data-title');
            const desc = btn.getAttribute('data-desc');
            const image = btn.getAttribute('data-image');
            const tech = btn.getAttribute('data-tech');
            const category = btn.getAttribute('data-category');
            const github = btn.getAttribute('data-github');
            const demo = btn.getAttribute('data-demo');

            modalTitle.textContent = title;
            modalDesc.textContent = desc;
            modalImage.src = image ? `static/${image}` : 'https://placehold.co/600x400/000000/FFFFFF?text=Project+Placeholder';
            modalCategory.textContent = category;

            // Generate technology badges
            modalTech.innerHTML = '';
            if (tech) {
                tech.split(',').forEach(item => {
                    const badge = document.createElement('span');
                    badge.className = 'px-3 py-1 bg-slate-100 text-black text-xs font-semibold rounded-none border border-slate-200 uppercase';
                    badge.textContent = item.trim();
                    modalTech.appendChild(badge);
                });
            }

            // GitHub repository URL
            if (github) {
                modalGithub.href = github;
                modalGithub.classList.remove('hidden');
            } else {
                modalGithub.classList.add('hidden');
            }

            // Live demo URL
            if (demo) {
                modalDemo.href = demo;
                modalDemo.classList.remove('hidden');
            } else {
                modalDemo.classList.add('hidden');
            }

            // Open Modal with transition classes
            modal.classList.add('modal-active');
            document.body.classList.add('overflow-hidden');
        });
    });

    if (modalClose && modal) {
        const closeModalFn = () => {
            modal.classList.remove('modal-active');
            document.body.classList.remove('overflow-hidden');
        };

        modalClose.addEventListener('click', closeModalFn);

        // Background overlay click close
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeModalFn();
            }
        });
    }

    // 8. Stats Number Counter Animation
    const animateCounter = (el) => {
        if (el.classList.contains('counter-done')) return;
        el.classList.add('counter-done');

        const targetText = el.getAttribute('data-target');
        const targetVal = parseInt(targetText);
        const suffix = targetText.replace(/[0-9]/g, ''); // Extract suffix e.g., '+'

        if (isNaN(targetVal)) return;

        let current = 0;
        const duration = 1500; // 1.5 seconds duration
        const stepTime = Math.max(Math.floor(duration / targetVal), 15);

        const timer = setInterval(() => {
            current += 1;
            el.textContent = current + suffix;
            if (current >= targetVal) {
                el.textContent = targetText;
                clearInterval(timer);
            }
        }, stepTime);
    };

    // 9. Scroll Reveal with IntersectionObserver & Skills bar animation
    const revealElements = document.querySelectorAll('.reveal');

    if ('IntersectionObserver' in window) {
        const revealObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                // If it is scrolled into view (threshold 10%)
                if (entry.isIntersecting) {
                    entry.target.classList.add('reveal-visible');

                    // Trigger progress bars fill if present inside entry
                    const progressBars = entry.target.querySelectorAll('.skills-progress-fill');
                    progressBars.forEach(bar => {
                        const pct = bar.getAttribute('data-percentage');
                        bar.style.width = `${pct}%`;
                    });

                    // Trigger stats number increment if present inside entry
                    const counters = entry.target.querySelectorAll('.stat-counter');
                    counters.forEach(counter => {
                        animateCounter(counter);
                    });

                    observer.unobserve(entry.target);
                }
            });
        }, {
            threshold: 0.08,
            rootMargin: '0px 0px -40px 0px'
        });

        revealElements.forEach(el => revealObserver.observe(el));
    } else {
        // Fallback for older browsers (instantly show elements & set widths/counters)
        revealElements.forEach(el => {
            el.classList.add('reveal-visible');
            const progressBars = el.querySelectorAll('.skills-progress-fill');
            progressBars.forEach(bar => {
                bar.style.width = `${bar.getAttribute('data-percentage')}%`;
            });
            const counters = el.querySelectorAll('.stat-counter');
            counters.forEach(counter => {
                counter.textContent = counter.getAttribute('data-target');
            });
        });
    }

    // 10. Auto close Alert Notifications after 5 seconds
    const alerts = document.querySelectorAll('.flash-alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 5000);
    });
});
