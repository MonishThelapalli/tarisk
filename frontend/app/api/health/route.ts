import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
    try {
        const backendResponse = await fetch('http://localhost:8000/health');
        const data = await backendResponse.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Error checking backend health:', error);
        return NextResponse.json({
            status: 'error',
            error: error instanceof Error ? error.message : 'Failed to connect to backend'
        }, { status: 500 });
    }
}