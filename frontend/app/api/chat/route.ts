import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
  const payload = await request.json();
  const { message, session_id } = payload;

    if (!message) {
      return NextResponse.json(
        {
          status: 'error',
          response: null,
          error: 'Message is required',
          session_id: null,
        },
        { status: 400 }
      );
    }

    const postPayload: any = { message };
    if (session_id) postPayload.session_id = session_id;

    const response = await fetch('http://127.0.0.1:8000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postPayload),
    });

    if (!response.ok) {
      const text = await response.text();
      return NextResponse.json({
        status: 'error',
        response: null,
        error: `Backend returned ${response.status}: ${text}`,
        session_id: null,
      }, { status: 502 });
    }

    const data = await response.json();

    return NextResponse.json({
      status: 'success',
      response: data.response || '',
      error: null,
      session_id: data.session_id || null,
    });
  } catch (error) {
    return NextResponse.json(
      {
        status: 'error',
        response: null,
        error: error instanceof Error ? error.message : 'An error occurred',
        session_id: null,
      },
      { status: 500 }
    );
  }
}
