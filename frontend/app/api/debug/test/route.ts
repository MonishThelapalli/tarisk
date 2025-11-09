import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest) {
    try {
        // Test connection to backend debug endpoint
        const backendResponse = await fetch('http://127.0.0.1:8000/api/debug/test', {
            headers: {
                'Accept': 'application/json',
            },
        });

        if (!backendResponse.ok) {
            throw new Error(`Backend responded with status: ${backendResponse.status}`);
        }

        const data = await backendResponse.json();
        
        return NextResponse.json({
            frontendStatus: "success",
            backendResponse: data,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        console.error('Debug test failed:', error);
        return NextResponse.json({
            status: 'error',
            error: error instanceof Error ? error.message : 'Failed to connect to backend',
            timestamp: new Date().toISOString()
        }, { status: 500 });
    }
}