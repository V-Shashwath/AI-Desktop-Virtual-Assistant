/**
 * Ultra-Lightweight Smooth Wave Animation
 * Optimized for maximum performance and smoothness
 */
class CustomSiriWave {
    constructor(options = {}) {
        this.container = options.container || document.getElementById('siri-container');
        this.width = options.width || 800;
        this.height = options.height || 200;
        this.amplitude = options.amplitude || 1;
        this.speed = options.speed || 0.4;
        this.autostart = options.autostart !== false;
        
        this.phase = 0;
        this.isRunning = false;
        this.animationFrameId = null;
        
        this.init();
        
        if (this.autostart) {
            this.start();
        }
    }
    
    init() {
        // Create canvas
        this.canvas = document.createElement('canvas');
        this.canvas.width = this.width;
        this.canvas.height = this.height;
        this.canvas.style.width = this.width + 'px';
        this.canvas.style.height = this.height + 'px';
        this.canvas.style.display = 'block';
        
        // Optimized context
        this.ctx = this.canvas.getContext('2d', {
            alpha: true,
            desynchronized: true
        });
        
        this.container.innerHTML = '';
        this.container.appendChild(this.canvas);
        
        // Center Y
        this.centerY = this.height / 2;
        
        // Pre-calculate values for performance
        this.widthHalf = this.width / 2;
        this.step = 4; // Larger step = fewer calculations = faster
        this.pointCount = Math.ceil(this.width / this.step) + 1;
        
        // Simple colorful wave layers - minimal
        this.waves = [
            { amplitude: 35, speed: 0.9, color: 'rgba(255, 100, 150, 0.35)', lineWidth: 1.5 },
            { amplitude: 45, speed: 1.0, color: 'rgba(100, 200, 255, 0.45)', lineWidth: 2 },
            { amplitude: 40, speed: 0.95, color: 'rgba(150, 255, 200, 0.55)', lineWidth: 2.2 },
            { amplitude: 50, speed: 1.05, color: 'rgba(255, 200, 100, 0.65)', lineWidth: 2.5 },
            { amplitude: 55, speed: 1.0, color: 'rgba(255, 255, 255, 0.95)', lineWidth: 2.8 }
        ];
    }
    
    drawWave(wave, phase) {
        // Top wave - single path
        this.ctx.beginPath();
        this.ctx.strokeStyle = wave.color;
        this.ctx.lineWidth = wave.lineWidth;
        this.ctx.lineCap = 'round';
        
        const freq = 0.02;
        const speedPhase = phase * wave.speed;
        let first = true;
        
        for (let x = 0; x <= this.width; x += this.step) {
            // Fast calculation
            const normalizedX = (x - this.widthHalf) / this.widthHalf;
            const absX = Math.abs(normalizedX);
            
            // Simple attenuation
            const att = absX < 1 ? (1 - absX * 0.85) : 0;
            
            if (att > 0.05) {
                // Single sine - fastest
                const y = this.centerY + Math.sin(x * freq + speedPhase) * wave.amplitude * this.amplitude * att;
                
                if (first) {
                    this.ctx.moveTo(x, y);
                    first = false;
                } else {
                    this.ctx.lineTo(x, y);
                }
            }
        }
        
        this.ctx.stroke();
        
        // Bottom wave - mirror
        this.ctx.beginPath();
        this.ctx.strokeStyle = wave.color;
        this.ctx.lineWidth = wave.lineWidth;
        this.ctx.lineCap = 'round';
        first = true;
        
        for (let x = 0; x <= this.width; x += this.step) {
            const normalizedX = (x - this.widthHalf) / this.widthHalf;
            const absX = Math.abs(normalizedX);
            const att = absX < 1 ? (1 - absX * 0.85) : 0;
            
            if (att > 0.05) {
                const y = this.centerY - Math.sin(x * freq + speedPhase) * wave.amplitude * this.amplitude * att;
                
                if (first) {
                    this.ctx.moveTo(x, y);
                    first = false;
                } else {
                    this.ctx.lineTo(x, y);
                }
            }
        }
        
        this.ctx.stroke();
    }
    
    draw() {
        // Fast clear
        this.ctx.clearRect(0, 0, this.width, this.height);
        
        // Draw waves
        const waveCount = this.waves.length;
        for (let i = 0; i < waveCount; i++) {
            this.drawWave(this.waves[i], this.phase);
        }
        
        // Fast phase update
        this.phase += this.speed * 0.08;
        if (this.phase > Math.PI * 2) {
            this.phase -= Math.PI * 2;
        }
    }
    
    animate() {
        if (!this.isRunning) return;
        
        this.draw();
        this.animationFrameId = requestAnimationFrame(() => this.animate());
    }
    
    start() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.phase = 0;
        this.animate();
    }
    
    stop() {
        this.isRunning = false;
        if (this.animationFrameId) {
            cancelAnimationFrame(this.animationFrameId);
            this.animationFrameId = null;
        }
    }
    
    setAmplitude(amplitude) {
        this.amplitude = Math.max(0, Math.min(1, amplitude));
    }
    
    setSpeed(speed) {
        this.speed = Math.max(0.1, Math.min(2, speed));
    }
    
    dispose() {
        this.stop();
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
    }
}

window.CustomSiriWave = CustomSiriWave;
