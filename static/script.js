// IPL Match Prediction App - JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Get elements
    const form = document.getElementById('prediction-form');
    const predictBtn = document.getElementById('predict-btn');
    const loadingOverlay = document.getElementById('loading-overlay');
    const resultContainer = document.getElementById('result-container');
    
    // Form validation and submission
    if (form) {
        form.addEventListener('submit', function(e) {
            // Check if batting team and bowling team are the same
            const battingTeam = form.querySelector('[name="batting_team"]').value;
            const bowlingTeam = form.querySelector('[name="bowling_team"]').value;
            
            if (battingTeam === bowlingTeam) {
                e.preventDefault();
                alert('Batting team and bowling team cannot be the same!');
                return false;
            }
            
            // Show loading overlay
            if (loadingOverlay) {
                loadingOverlay.classList.add('active');
                
                // Hide loading overlay after form submission (for better UX if page reloads)
                setTimeout(() => {
                    loadingOverlay.classList.remove('active');
                }, 10000); // Timeout as a fallback
            }
            
            return true;
        });
    }
    
    // Team selection validation
    const battingTeamSelect = document.querySelector('[name="batting_team"]');
    const bowlingTeamSelect = document.querySelector('[name="bowling_team"]');
    
    if (battingTeamSelect && bowlingTeamSelect) {
        // Function to update available teams to prevent selecting the same team
        const updateAvailableTeams = function(selectedTeam, targetSelect) {
            const options = targetSelect.querySelectorAll('option');
            
            options.forEach(option => {
                if (option.value && option.value === selectedTeam) {
                    option.disabled = true;
                } else if (option.value) {
                    option.disabled = false;
                }
            });
        };
        
        // Add event listeners for team selection changes
        battingTeamSelect.addEventListener('change', function() {
            updateAvailableTeams(this.value, bowlingTeamSelect);
        });
        
        bowlingTeamSelect.addEventListener('change', function() {
            updateAvailableTeams(this.value, battingTeamSelect);
        });
        
        // Initialize on page load
        if (battingTeamSelect.value) {
            updateAvailableTeams(battingTeamSelect.value, bowlingTeamSelect);
        }
        
        if (bowlingTeamSelect.value) {
            updateAvailableTeams(bowlingTeamSelect.value, battingTeamSelect);
        }
        
        // Fix for select dropdown text visibility
        const selectBoxes = document.querySelectorAll('select.form-control');
        selectBoxes.forEach(select => {
            select.style.color = 'white';
            const options = select.querySelectorAll('option');
            options.forEach(option => {
                option.style.color = 'white';
                option.style.backgroundColor = 'var(--primary)';
            });
        });
    }
    
    // Overs validation - max 20 overs
    const oversInput = document.querySelector('[name="overs"]');
    if (oversInput) {
        oversInput.addEventListener('input', function() {
            const value = parseFloat(this.value);
            if (value > 20) {
                this.value = 20;
            }
            
            // Ensure proper decimal format for overs (only .0 to .5)
            const decimalPart = value % 1;
            if (decimalPart > 0.5) {
                this.value = Math.floor(value) + 0.5;
            }
        });
    }
    
    // Wickets validation - max 10 wickets
    const wicketsInput = document.querySelector('[name="wickets"]');
    if (wicketsInput) {
        wicketsInput.addEventListener('input', function() {
            const value = parseInt(this.value);
            if (value > 10) {
                this.value = 10;
            }
        });
    }
    
    // Form field animations
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            group.style.transition = 'all 0.5s ease';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 100 * index);
    });
    
    // Fix for toss impact display - remove curly braces if present
    const tossStatElement = document.querySelector('.insight-card:nth-child(2) .insight-value');
    if (tossStatElement) {
        const text = tossStatElement.textContent;
        if (text.includes('{') || text.includes('}')) {
            // Remove curly braces and any whitespace
            const cleanedText = text.replace(/[{}]/g, '').trim();
            tossStatElement.textContent = cleanedText;
        }
    }
    
    // Dynamic insight cards
    const insightCards = document.querySelectorAll('.insight-card');
    if (insightCards.length > 0) {
        insightCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 200 * index);
        });
    }
    
    // Dynamic recommendations animation
    const recommendations = document.querySelectorAll('.recommendation-item');
    if (recommendations.length > 0) {
        recommendations.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.5s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, 150 * index);
        });
    }
    
    // Animation for ring progress
    const animateRingProgress = function() {
        const ringProgressElements = document.querySelectorAll('.ring-progress');
        
        ringProgressElements.forEach(ring => {
            const finalDashArray = ring.getAttribute('stroke-dasharray');
            ring.setAttribute('stroke-dasharray', '0, 251');
            
            setTimeout(() => {
                ring.style.transition = 'stroke-dasharray 1.5s ease-out';
                ring.setAttribute('stroke-dasharray', finalDashArray);
            }, 300);
        });
    };
    
    // Initialize ring animation if they exist on the page
    const rings = document.querySelectorAll('.ring-progress');
    if (rings.length > 0) {
        animateRingProgress();
    }
    
    // Add interactivity to the city dropdown to display historical data
    const citySelect = document.querySelector('[name="city"]');
    if (citySelect) {
        citySelect.addEventListener('change', function() {
            // You could use this to dynamically update some city-related information
            // This would be integrated with backend data in a real implementation
            console.log('Selected city:', this.value);
        });
    }
    
    // Form validation for ensuring all required fields are filled
    const validateForm = function() {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value) {
                isValid = false;
                field.classList.add('error');
            } else {
                field.classList.remove('error');
            }
        });
        
        return isValid;
    };
    
    // Add validation feedback on input change
    const requiredFields = form ? form.querySelectorAll('[required]') : [];
    requiredFields.forEach(field => {
        field.addEventListener('change', function() {
            if (!this.value) {
                this.classList.add('error');
            } else {
                this.classList.remove('error');
            }
        });
    });
    
    // Enhance the cricket animation when prediction is running
    let animationInterval;
    
    const enhanceCricketAnimation = function() {
        const bat = document.querySelector('.bat');
        const ball = document.querySelector('.ball');
        
        if (bat && ball) {
            clearInterval(animationInterval);
            
            let ballPosition = 0;
            let batAngle = -30;
            let batDirection = 1;
            let hitBall = false;
            
            animationInterval = setInterval(() => {
                // Animate bat swinging
                batAngle += 2 * batDirection;
                if (batAngle >= 30) batDirection = -1;
                if (batAngle <= -30) {
                    batDirection = 1;
                    hitBall = false;
                }
                
                bat.style.transform = `rotate(${batAngle}deg)`;
                
                // Animate ball movement
                if (batAngle > 0 && !hitBall) {
                    hitBall = true;
                    ballPosition = 0;
                }
                
                if (hitBall) {
                    ballPosition += 5;
                    ball.style.transform = `translateY(-${ballPosition}px) translateX(-${ballPosition * 1.5}px)`;
                    
                    if (ballPosition > 100) {
                        ballPosition = 0;
                        ball.style.transform = 'translateY(0) translateX(0)';
                    }
                }
            }, 50);
        }
    };
    
    // Initialize the enhanced cricket animation when loading overlay is shown
    if (loadingOverlay) {
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.attributeName === 'class') {
                    if (loadingOverlay.classList.contains('active')) {
                        enhanceCricketAnimation();
                    } else {
                        clearInterval(animationInterval);
                    }
                }
            });
        });
        
        observer.observe(loadingOverlay, { attributes: true });
    }
    
    // Add tooltip functionality and animations for team rings
    const teamRings = document.querySelectorAll('.team-ring');
    teamRings.forEach(ring => {
        ring.addEventListener('mouseenter', function() {
            const progress = this.querySelector('.ring-progress');
            const text = this.querySelector('.ring-text');
            const teamName = this.querySelector('.team-name');
            
            if (progress) progress.style.strokeWidth = '10';
            if (text) text.style.fontSize = '18';
            if (teamName) {
                teamName.style.transform = 'scale(1.1)';
                teamName.style.color = '#ff9800';
            }
        });
        
        ring.addEventListener('mouseleave', function() {
            const progress = this.querySelector('.ring-progress');
            const text = this.querySelector('.ring-text');
            const teamName = this.querySelector('.team-name');
            
            if (progress) progress.style.strokeWidth = '8';
            if (text) text.style.fontSize = '16';
            if (teamName) {
                teamName.style.transform = 'scale(1)';
                teamName.style.color = 'white';
            }
        });
    });
    
    // Add tooltip functionality for insights
    const insightValues = document.querySelectorAll('.insight-value');
    insightValues.forEach(value => {
        value.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.1)';
            this.style.color = '#ff9800';
        });
        
        value.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
            this.style.color = '';
        });
    });
});