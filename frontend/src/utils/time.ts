import { useI18n } from 'vue-i18n';

/**
 * Time related utility functions
 */

/**
 * Convert timestamp to relative time (e.g., minutes ago, hours ago, days ago)
 * @param timestamp Timestamp (seconds)
 * @returns Formatted relative time string
 */
export const formatRelativeTime = (timestamp: number): string => {
  const { t } = useI18n();
  const now = Math.floor(Date.now() / 1000);
  const diffSec = now - timestamp;
  const diffMin = Math.floor(diffSec / 60);
  const diffHour = Math.floor(diffMin / 60);
  const diffDay = Math.floor(diffHour / 24);
  const diffMonth = Math.floor(diffDay / 30);
  const diffYear = Math.floor(diffMonth / 12);

  if (diffSec < 60) {
    return t('Just now');
  } else if (diffMin < 60) {
    return `${diffMin} ${t('minutes ago')}`;
  } else if (diffHour < 24) {
    return `${diffHour} ${t('hours ago')}`;
  } else if (diffDay < 30) {
    return `${diffDay} ${t('days ago')}`;
  } else if (diffMonth < 12) {
    return `${diffMonth} ${t('months ago')}`;
  } else {
    return `${diffYear} ${t('years ago')}`;
  }
}; 