import {
  availableAlbumsAlbumsGet,
  captureImageToAlbum,
  createAlbumAlbumsPost,
  getAlbumInfo,
  getQrCodesQrCodesGet,
  lastImageForAlbumAlbumsAlbumNameLastImageGet,
} from "./api";
import { client } from "./api/client.gen";
import type {
  AlbumCaptureResponse,
  AlbumCreatedResponse,
  AlbumInfoResponse,
  AvailableAlbumsResponse,
  GetQrCodesQrCodesGetResponses,
  LastImageResponse,
} from "./api";

export type ApiError = { error: string };
export type Result<T> = T | ApiError;

const resolveApiBaseUrl = (): string => {
  return window.location.origin;
};

client.setConfig({ baseUrl: resolveApiBaseUrl() });

export const isApiError = (value: unknown): value is ApiError =>
  typeof value === "object" &&
  value !== null &&
  "error" in value &&
  typeof (value as { error: unknown }).error === "string";

const normalizeError = (value: unknown): ApiError =>
  isApiError(value) ? value : { error: "Unknown error" };

const unwrap = async <T>(promise: Promise<unknown>): Promise<Result<T>> => {
  const result = await promise;
  if (result && typeof result === "object") {
    const maybeResult = result as { data?: unknown; error?: unknown };
    if (maybeResult.data !== undefined) {
      return maybeResult.data as T;
    }
    if (maybeResult.error !== undefined) {
      return normalizeError(maybeResult.error);
    }
  }
  return { error: "Unknown error" };
};

export const get_available_album_data = async (): Promise<Result<AvailableAlbumsResponse>> =>
  unwrap<AvailableAlbumsResponse>(availableAlbumsAlbumsGet());

export const get_album_info = async (album_name: string): Promise<Result<AlbumInfoResponse>> =>
  unwrap<AlbumInfoResponse>(getAlbumInfo({ path: { album_name } }));

export const get_last_image_url = async (album_name: string): Promise<Result<LastImageResponse>> =>
  unwrap<LastImageResponse>(lastImageForAlbumAlbumsAlbumNameLastImageGet({ path: { album_name } }));

export const capture_image_to_album = async (album_name: string): Promise<Result<AlbumCaptureResponse>> =>
  unwrap<AlbumCaptureResponse>(captureImageToAlbum({ path: { album_name } }));

export const create_or_update_album = async (
  album_name: string,
  description?: string
): Promise<Result<AlbumCreatedResponse>> =>
  unwrap<AlbumCreatedResponse>(createAlbumAlbumsPost({ body: { album_name, description } }));

export const get_qr_codes = async (): Promise<Result<GetQrCodesQrCodesGetResponses[200]>> =>
  unwrap<GetQrCodesQrCodesGetResponses[200]>(getQrCodesQrCodesGet());
