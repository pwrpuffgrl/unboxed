import Logo from './Logo';

export default function Header() {
  return (
    <header className="bg-gray-800 shadow-lg border-b border-gray-700 flex-shrink-0 min-h-[88px]">
            <div className="py-6 px-6 pr-4 sm:pr-6 lg:pr-8">
        <div className="hidden xl:flex  gap-4">
          <Logo size="md" showText={false} />
          <div>
            <h1 className="text-3xl font-bold text-white">Unboxed</h1>
            <p className="text-gray-300 mt-1">Talk to your knowledge</p>
          </div>
        </div>
      </div>
    </header>
  );
} 