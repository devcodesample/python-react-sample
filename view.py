import random
import re
import string
from datetime import datetime, timedelta

from nltk import word_tokenize, pos_tag, WordNetLemmatizer
from nltk.corpus import stopwords


def make_filters(time_frame_filter: str = None, country_filter: str = None):
    """
    Creates and returns filters
    
    :param time_frame_filter: filter param
    :param country_filter: filter param
    :return: filters
    """
    filters = []
    if time_frame_filter:
        filter_type = 'time_frame'
        filter_data = time_frame_filter.split('_')
        if len(filter_data) == 3:
            if filter_data[2] == 'hours':
                delta = timedelta(hours=int(filter_data[1]))
                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime.now() - delta,
                        'lte': datetime.now(),
                    }
                )
            elif filter_data[2] == 'days':
                delta = timedelta(days=int(filter_data[1]))
                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime.now() - delta,
                        'lte': datetime.now(),
                    }
                )
        elif len(filter_data) == 2:
            if time_frame_filter == 'past_year':
                delta = timedelta(days=365)
                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime.now() - delta,
                        'lte': datetime.now(),
                    }
                )
            elif time_frame_filter == 'year_to_date':
                current_year = datetime.today().year
                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime(current_year, 1, 1),
                        'lte': datetime.now()
                    }
                )
            elif time_frame_filter == 'this_quarter':
                today = datetime.today()
                current_quarter = ((today.month - 1) // 3) + 1

                quarter_month = None
                if current_quarter == 1:
                    quarter_month = 1
                elif current_quarter == 2:
                    quarter_month = 4
                elif current_quarter == 3:
                    quarter_month = 7
                elif current_quarter == 4:
                    quarter_month = 10

                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime(today.year, quarter_month, 1),
                        'lte': datetime.now(),
                    }
                )
            elif time_frame_filter == 'this_month':
                today = datetime.today()
                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime(today.year, today.month, 1),
                        'lte': datetime.now(),
                    }
                )
            elif time_frame_filter == 'this_week':
                today = datetime.today()
                delta = timedelta(days=today.weekday())
                filters.append(
                    {
                        'type': filter_type,
                        'gte': datetime.now() - delta,
                        'lte': datetime.now(),
                    }
                )

    if country_filter:
        filter_type = 'countries'
        filter_data = country_filter.split(',')
        filters.append(
            {
                'type': filter_type,
                'countries': filter_data
            }
        )

    return filters


def without_keys(d, keys):
    """
    Returns the provided dictionary without specified keys

    :param d: dictionary
    :param keys: keys to remove
    :return: dictionary after removing provided keys
    """
    return {x: d[x] for x in d if x not in keys}


def remove_noise(statement):
    """
    Removes stop words and symbols

    :param statement:
    :return:
    """
    cleaned_tokens = []
    stop_words = stopwords.words('english')
    tokens = word_tokenize(statement)
    for token, tag in pos_tag(tokens):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*(),]|'
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith('NN'):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        # noinspection SpellCheckingInspection
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 2 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())

        random.shuffle(cleaned_tokens)
    return cleaned_tokens


def get_nps_segment_data(pro_detract_count):
    """
    Returns NPS Segment data for a Survey / Company

    :param pro_detract_count: dict
    :return: nps_segment_data
    """
    nps_segment_data = {
        'promoters': {
            'count': 0,
            'percent': 0.0
        },
        'passives': {
            'count': 0,
            'percent': 0.0
        },
        'detractors': {
            'count': 0,
            'percent': 0.0
        }
    }

    nps_segment = pro_detract_count

    if nps_segment['total'] == 0:
        return nps_segment_data

    promoters_percentage = (nps_segment['promoters'] / nps_segment['total']) * 100
    passives_percentage = (nps_segment['passives'] / nps_segment['total']) * 100
    detractors_percentage = (nps_segment['detractors'] / nps_segment['total']) * 100

    nps_segment_data['promoters']['count'] = int(round(nps_segment['promoters']))
    nps_segment_data['promoters']['percent'] = round(promoters_percentage, 2)

    nps_segment_data['passives']['count'] = int(round(nps_segment['passives']))
    nps_segment_data['passives']['percent'] = round(passives_percentage, 2)

    nps_segment_data['detractors']['count'] = int(round(nps_segment['detractors']))
    nps_segment_data['detractors']['percent'] = round(detractors_percentage, 2)

    return nps_segment_data


def get_nps_trend(company=None, survey=None):
    """
    Returns NPS Trend data for a Survey / Company

    :param survey: Survey Object
    :param company: Company Object
    :return: plotted_data
    """
    if company and survey:
        raise AttributeError('Either company or survey should be provided')

    plotted_data = {}

    if company:
        trend = NpsChange.objects.filter(company=company)
    elif survey:
        trend = NpsChange.objects.filter(survey=survey)
    else:
        raise AttributeError('Required either company or survey')
    for change in trend:
        date_time = str(change.date_time).split(' ')[0]
        plotted_data[date_time] = change.nps

    return plotted_data


def get_nps_volume_trend(survey):
    """
    Returns NPS Volume Trend data for a Survey

    :param survey: Survey Object
    :return: trend data - list
    """
    promoters_data = []
    passives_data = []
    detractors_data = []

    trend_data = NpsChange.objects.order_by('id').filter(survey=survey)

    for trend in trend_data:
        date_time = str(trend.date_time)
        date_time = date_time.split(' ')[0]
        date_time = date_time.split('-')

        year = int(date_time[0])
        month = int(date_time[1])
        day = int(date_time[2])

        date_time = datetime(year, month, day)

        promoters_data.append(
            [
                date_time,
                trend.promoters
            ]
        )
        passives_data.append(
            [
                date_time,
                trend.passives
            ]
        )
        detractors_data.append(
            [
                date_time,
                trend.detractors
            ]
        )

    series = [
        {
            'name': 'Promoters',
            'data': promoters_data
        },
        {
            'name': 'Passives',
            'data': passives_data
        },
        {
            'name': 'Detractors',
            'data': detractors_data
        }
    ]
    return series


def calculate_nps(promoters, detractors, respondents):
    """
    Calculates NPS score
    :param promoters:
    :param detractors:
    :param respondents:
    :return:
    """
    if respondents == 0:
        return 0
    promoters_percent = (promoters / respondents) * 100
    detractors_percent = (detractors / respondents) * 100
    nps = promoters_percent - detractors_percent
    return int(round(nps))


def get_grade_sum(response_score):
    """
    Returns sum of response score

    :param response_score: dict
    :return: int
    """
    grade = 0
    grade_sum = 0
    if 'score_data' in response_score:
        for score in response_score['score_data']:
            if score != 0:
                grade_sum += grade * score
            grade += 1
    return grade_sum


class IsAuthenticatedOrWriteOnly(BasePermission):
    """
    The request is authenticated as a user, or is a write-only request.
    """

    def has_permission(self, request, view):
        # noinspection PyPep8Naming
        WRITE_METHODS = ["POST", ]

        return (
                request.method in WRITE_METHODS or
                request.user and
                request.user.is_authenticated
        )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrWriteOnly]

    def create(self, request, *args, **kwargs):
        # Remove this function to return actual user data on registration
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response({"message": "Registration was successful!"},
                        status=status.HTTP_201_CREATED, headers=headers)


class AuthProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint for logged in user profiles.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if self.action == 'list':
            return self.queryset.filter(user=self.request.user)
        return self.queryset


class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for companies
    """
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        :param serializer:
        :return:
        """
        sharing_pin_rand = random.randint(10000, 99999)
        serializer.save(sharing_pin=sharing_pin_rand)
