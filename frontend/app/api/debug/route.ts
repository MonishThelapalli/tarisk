import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
    // Try to connect to backend
    try {
        const backendResponse = await fetch('http://127.0.0.1:8000/health');
        const backendData = await backendResponse.json();
        
        return NextResponse.json({
            status: 'success',
            backend: backendData,
            message: 'Debug route working'
        });
    } catch (error) {
        return NextResponse.json({
            status: 'error',
            error: error instanceof Error ? error.message : 'Unknown error',
            message: 'Failed to connect to backend'
        });
    }
}