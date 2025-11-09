"use client";
import { CheckIcon, CopyIcon } from 'lucide-react';
import React from 'react';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dracula } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { vscDarkPlus } from 'react-syntax-highlighter/dist/esm/styles/prism';
import { Button } from '@/components/ui/button';
import { toast } from 'sonner';
import { useTheme } from 'next-themes';

interface ButtonCodeblockProps {
  code: string;
  lang: string;
}

export default function CodeDisplayBlock({ code, lang }: ButtonCodeblockProps) {
  const [isCopied, setisCopied] = React.useState(false);
  const { theme } = useTheme();

  const copyToClipboard = () => {
    navigator.clipboard.writeText(code);
    setisCopied(true);
    toast.success('Code copied to clipboard!');
    setTimeout(() => {
      setisCopied(false);
    }, 1500);
  };

  const [failed, setFailed] = React.useState(false);

  const fallback = (
    <pre className="whitespace-pre-wrap overflow-auto p-3 rounded-md bg-gray-50 dark:bg-[#222] text-sm">
      <code>{code}</code>
    </pre>
  );

  const renderHighlighter = () => {
    if (failed) return fallback;
    try {
      return (
        <SyntaxHighlighter
          style={theme === 'dark' ? dracula : vscDarkPlus}
          language={lang ?? 'text'}
          showLineNumbers={false}
          customStyle={theme === 'dark' ? { background: '#303033' } : { background: '#fcfcfc' }}
        >
          {code}
        </SyntaxHighlighter>
      );
    } catch (err) {
      // If the highlighter fails (chunk load error etc.) fall back to plain pre
      // set state so subsequent renders show fallback
      console.error('Highlighter render failed, falling back to plain pre:', err);
      setFailed(true);
      return fallback;
    }
  };

  return (
    <div className="relative flex flex-col   text-start  ">
      <Button onClick={copyToClipboard} variant="ghost" size="icon" className="h-5 w-5 absolute top-2 right-2">
        {isCopied ? (
          <CheckIcon className="w-4 h-4 scale-100 transition-all" />
        ) : (
          <CopyIcon className="w-4 h-4 scale-100 transition-all" />
        )}
      </Button>
      <div className="w-full">{renderHighlighter()}</div>
    </div>
  );
}
