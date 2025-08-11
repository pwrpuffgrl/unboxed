import { LogoProps } from '../types';

export default function Logo({ size = 'md', showText = true }: LogoProps) {
  const sizeClasses = {
    sm: 'w-8 h-8',
    md: 'w-12 h-12', 
    lg: 'w-16 h-16'
  };

  const textSizes = {
    sm: 'text-sm',
    md: 'text-lg',
    lg: 'text-xl'
  };

  return (
    <div className="flex flex-col items-center gap-2">
      {/* Icon */}
      <div className={`${sizeClasses[size]} relative`}>
        {/* Background circle */}
        <div className="w-full h-full bg-cyan-500 rounded-full flex items-center justify-center">
          {/* Isometric cube */}
          <svg 
            viewBox="0 0 24 24" 
            className="w-4/5 h-4/5"
            fill="none"
          >
            {/* Top face */}
            <path 
              d="M12 2L21 7L12 12L3 7L12 2Z" 
              fill="white" 
              fillOpacity="0.2"
            />
            {/* Right face */}
            <path 
              d="M21 7L21 16L12 21L12 12L21 7Z" 
              fill="white" 
              fillOpacity="0.1"
            />
            {/* Left face */}
            <path 
              d="M3 7L3 16L12 21L12 12L3 7Z" 
              fill="white" 
              fillOpacity="0.15"
            />
            
            {/* All cube edges */}
            <path d="M12 2L21 7" stroke="white" strokeWidth="1" />
            <path d="M21 7L21 16" stroke="white" strokeWidth="1" />
            <path d="M21 16L12 21" stroke="white" strokeWidth="1" />
            <path d="M12 21L3 16" stroke="white" strokeWidth="1" />
            <path d="M3 16L3 7" stroke="white" strokeWidth="1" />
            <path d="M3 7L12 2" stroke="white" strokeWidth="1" />
            <path d="M12 2L12 12" stroke="white" strokeWidth="1" />
            <path d="M12 12L21 7" stroke="white" strokeWidth="1" />
            <path d="M12 12L3 7" stroke="white" strokeWidth="1" />
            <path d="M12 12L12 21" stroke="white" strokeWidth="1" />
            <path d="M12 12L21 16" stroke="white" strokeWidth="1" />
            <path d="M12 12L3 16" stroke="white" strokeWidth="1" />
          </svg>
        </div>
      </div>

      {/* Text */}
      {showText && (
        <span className={`${textSizes[size]} font-bold text-cyan-500`}>
          Unboxed
        </span>
      )}
    </div>
  );
} 