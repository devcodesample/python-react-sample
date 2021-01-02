def get_nps_segment_data(pro_detract_count):
    """
    Returns NPS Segment data for a Survey / Company

    :param survey: pro_detract_count
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
        sharing_pin_rand = randint(10000, 99999)
        serializer.save(sharing_pin=sharing_pin_rand)

