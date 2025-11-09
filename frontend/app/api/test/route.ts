import { NextResponse } from 'next/server';

export async function GET() {
    try {
        // Test basic connectivity
        const response = await fetch('http://127.0.0.1:8000/api/test', {
            method: 'GET',
            headers: {
                'Accept': 'application/json',
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            return NextResponse.json({
                status: 'error',
                error: errorData,
                statusCode: response.status,
                statusText: response.statusText
            }, { status: response.status });
        }

        const data = await response.json();
        return NextResponse.json(data);
    } catch (error) {
        console.error('Connection test failed:', error);
        return NextResponse.json({
            status: 'error',
            message: 'Failed to connect to backend',
            error: error instanceof Error ? error.message : String(error)
        }, { status: 500 });
    }
}