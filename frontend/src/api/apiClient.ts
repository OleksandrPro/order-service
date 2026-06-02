export async function handleResponse<T>(res: Response): Promise<T> {
  if (!res.ok) {
    let errorMessage = `HTTP error! status: ${res.status}`;
    try {
      const errorData = await res.json();
      errorMessage = errorData.message || errorData.detail || errorMessage;
    } catch (e) {
      // Ignore parsing error
    }
    throw new Error(errorMessage);
  }
  return res.json();
}