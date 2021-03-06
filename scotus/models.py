from django.db import models

from clerk import maps
from scotus import utils


class NaturalCourt(utils.BaseScotusModel):
    """
    Represents a single natural court, e.g., a combination of Justices in their seats.
    When a Justice leaves / enters the court, a new natural court will be formed.
    """
    naturalcourt = models.IntegerField(primary_key=True)
    chief = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        """
        Django Meta class.
        """
        managed = False
        db_table = 'naturalcourts'

    def __unicode__(self):
        return "%s - %s" % (self.naturalcourt, self.chief)

    def court_terms(self):
        """
        Returns a dictionary for each term in a natural court and the MQ score for that term.
        """
        return [
            {"term": f.term, "score": f.martin_quinn_score}\
            for f in CourtTerm.objects.filter(naturalcourt=self.naturalcourt)
        ]


class CourtTerm(utils.BaseScotusModel):
    """
    Represents a single term of the court for the purposes
    of aggregating the Martin-Quinn score for this court
    on this term.
    """
    term = models.CharField(max_length=255, primary_key=True)
    med = models.FloatField(blank=True, null=True)
    med_sd = models.FloatField(blank=True, null=True)
    min = models.FloatField(blank=True, null=True)
    max = models.FloatField(blank=True, null=True)
    justice = models.CharField(max_length=255, blank=True, null=True)
    just_pr = models.FloatField(blank=True, null=True)
    harlan = models.FloatField(blank=True, null=True)
    black = models.FloatField(blank=True, null=True)
    douglas = models.FloatField(blank=True, null=True)
    stewart = models.FloatField(blank=True, null=True)
    marshall = models.FloatField(blank=True, null=True)
    brennan = models.FloatField(blank=True, null=True)
    white = models.FloatField(blank=True, null=True)
    warren = models.FloatField(blank=True, null=True)
    clark = models.FloatField(blank=True, null=True)
    frankfurter = models.FloatField(blank=True, null=True)
    whittaker = models.FloatField(blank=True, null=True)
    burton = models.FloatField(blank=True, null=True)
    reed = models.FloatField(blank=True, null=True)
    fortas = models.FloatField(blank=True, null=True)
    goldberg = models.FloatField(blank=True, null=True)
    minton = models.FloatField(blank=True, null=True)
    jackson = models.FloatField(blank=True, null=True)
    burger = models.FloatField(blank=True, null=True)
    blackmun = models.FloatField(blank=True, null=True)
    powell = models.FloatField(blank=True, null=True)
    rehnquist = models.FloatField(blank=True, null=True)
    stevens = models.FloatField(blank=True, null=True)
    oconnor = models.FloatField(blank=True, null=True)
    scalia = models.FloatField(blank=True, null=True)
    kennedy = models.FloatField(blank=True, null=True)
    souter = models.FloatField(blank=True, null=True)
    thomas = models.FloatField(blank=True, null=True)
    ginsburg = models.FloatField(blank=True, null=True)
    breyer = models.FloatField(blank=True, null=True)
    rutledge = models.FloatField(blank=True, null=True)
    murphy = models.FloatField(blank=True, null=True)
    vinson = models.FloatField(blank=True, null=True)
    byrnes = models.FloatField(blank=True, null=True)
    sutherland = models.FloatField(blank=True, null=True)
    cardozo = models.FloatField(blank=True, null=True)
    brandeis = models.FloatField(blank=True, null=True)
    butler = models.FloatField(blank=True, null=True)
    mcreynolds = models.FloatField(blank=True, null=True)
    hughes = models.FloatField(blank=True, null=True)
    oroberts = models.FloatField(blank=True, null=True)
    stone = models.FloatField(blank=True, null=True)
    roberts = models.FloatField(blank=True, null=True)
    alito = models.FloatField(blank=True, null=True)
    sotomayor = models.FloatField(blank=True, null=True)
    kagan = models.FloatField(blank=True, null=True)
    objects = models.Manager()

    class Meta:
        """
        Django Meta class.
        """
        managed = False
        db_table = 'courts'

    def __unicode__(self):
        return "%s %s" % (self.term, self.med)

    def justice_terms(self):
        """
        Return Django JusticeTerm model objects for this term.
        """
        return JusticeTerm.objects.filter(term=self.term)


class Case(utils.BaseScotusModel):
    """
    Represents a single merits case before the court.
    Largely derived from SCDB data.
    Use MeritsCase.valid when doing votes because
    combined cases might appear as duplicates.
    """
    term = models.CharField(max_length=255, null=True, blank=True)
    docket = models.CharField(max_length=255, null=True, blank=True)
    caseid = models.CharField(max_length=255, null=True, blank=True)
    docketid = models.CharField(max_length=255, null=True, blank=True)
    caseissuesid = models.CharField(max_length=255, primary_key=True)
    datedecision = models.DateField(blank=True, null=True)
    decisiontype = models.CharField(
        choices=maps.DECISION_TYPE_CHOICES, max_length=255, null=True, blank=True)
    uscite = models.CharField(max_length=255, null=True, blank=True)
    sctcite = models.CharField(max_length=255, null=True, blank=True)
    ledcite = models.CharField(max_length=255, null=True, blank=True)
    lexiscite = models.CharField(max_length=255, null=True, blank=True)
    naturalcourt = models.CharField(
        choices=maps.NATURAL_COURT_CHOICES, max_length=255, db_index=True)
    chief = models.CharField(max_length=255, null=True, blank=True)
    casename = models.CharField(max_length=255, null=True, blank=True)
    dateargument = models.DateField(blank=True, null=True)
    # daterearg = models.DateField(blank=True, null=True)
    petitioner = models.CharField(
        choices=maps.PETITIONER_RESPONDENT_CHOICES, max_length=255, db_index=True, blank=True, null=True)
    petitionerstate = models.CharField(
        choices=maps.STATE_CHOICES, max_length=255, blank=True, null=True)
    respondent = models.CharField(
        choices=maps.PETITIONER_RESPONDENT_CHOICES, max_length=255, blank=True, null=True)
    respondentstate = models.CharField(
        choices=maps.STATE_CHOICES, max_length=255, blank=True, null=True)
    jurisdiction = models.CharField(
        choices=maps.JURISDICTION_CHOICES, max_length=255, db_index=True, null=True, blank=True)
    adminaction = models.CharField(
        choices=maps.ADMINISTRATIVE_ACTION_CHOICES, max_length=255, null=True, blank=True)
    adminactionstate = models.CharField(
        choices=maps.STATE_CHOICES, max_length=255, null=True, blank=True)
    threejudgefdc = models.CharField(
        choices=maps.THREE_JUDGE_DISTRICT_COURT_CHOICES, max_length=255, null=True, blank=True)
    caseorigin = models.CharField(
        choices=maps.CASE_ORIGIN_CHOICES, max_length=255, null=True, blank=True)
    caseoriginstate = models.CharField(
        choices=maps.STATE_CHOICES, max_length=255, null=True, blank=True)
    casesource = models.CharField(
        choices=maps.CASE_ORIGIN_CHOICES, max_length=255, null=True, blank=True)
    casesourcestate = models.CharField(
        choices=maps.STATE_CHOICES, max_length=255, null=True, blank=True)
    certreason = models.CharField(
        choices=maps.CERT_REASON_OPTIONS, max_length=255, null=True, blank=True)
    lcdisagreement = models.CharField(
        choices=maps.LOWER_COURT_AGREEMENT_CHOICES, max_length=255, null=True, blank=True)
    lcdisposition = models.CharField(
        choices=maps.LOWER_COURT_DISPOSITION_CHOICES, max_length=255, null=True, blank=True)
    # lcdispositiondirection = models.CharField(
    #    choices=maps.DECISION_DIRECTION_CHOICES, max_length=255, null=True, blank=True)
    # lcdecisiondirection = models.CharField(
    #    choices=maps.DECISION_DIRECTION_CHOICES, max_length=255, null=True, blank=True)
    declarationuncon = models.CharField(
        choices=maps.UNCONSTITUTIONALITY_CHOICES, max_length=255, null=True, blank=True)
    casedisposition = models.CharField(
        choices=maps.CASE_DISPOSITION_CHOICES, max_length=255, null=True, blank=True)
    casedispositionunusual = models.CharField(
        choices=maps.CASE_DISPOSITION_UNUSUAL_CHOICES, max_length=255, null=True, blank=True)
    partywinning = models.CharField(
        choices=maps.WINNING_PARTY_CHOICES, max_length=255, null=True, blank=True)
    precedentalteration = models.CharField(
        choices=maps.PRECEDENT_ALTERATION_CHOICES, max_length=255, null=True, blank=True)
    voteunclear = models.CharField(
        choices=maps.VOTE_UNCLEAR_CHOICES, max_length=255, null=True, blank=True)
    issue = models.CharField(
        choices=maps.ISSUE_CHOICES, max_length=255, blank=True, null=True, db_index=True)
    issuearea = models.CharField(
        choices=maps.ISSUE_AREA_CHOICES, max_length=255, blank=True, null=True, db_index=True)
    decisiondirection = models.CharField(
        choices=maps.DECISION_DIRECTION_CHOICES, 
        max_length=255, db_index=True, null=True, blank=True)
    decisiondirectiondissent = models.CharField(
        choices=maps.DECISION_DIRECTION_DISSENT_CHOICES,
        max_length=255, db_index=True, null=True, blank=True)
    authoritydecision1 = models.CharField(
        choices=maps.DECISION_AUTHORITY_CHOICES, max_length=255, null=True, blank=True)
    authoritydecision2 = models.CharField(
        choices=maps.DECISION_AUTHORITY_CHOICES, max_length=255, null=True, blank=True)
    lawtype = models.CharField(
        choices=maps.DECISION_LAW_TYPE_CHOICES, max_length=255, null=True, blank=True)
    lawsupp = models.CharField(
        choices=maps.LAW_SUPP_CHOICES, max_length=255, null=True, blank=True)
    lawminor = models.CharField(max_length=255, null=True, blank=True)
    majopinwriter = models.CharField(max_length=255, null=True, blank=True)
    majopinassigner = models.CharField(max_length=255, null=True, blank=True)
    splitvote = models.CharField(
        choices=maps.SPLIT_VOTE_CHOICES, max_length=255, null=True, blank=True)
    majvotes = models.CharField(max_length=255, db_index=True)
    minvotes = models.CharField(max_length=255, db_index=True)
    weighted_majvotes = models.IntegerField(blank=True, null=True)
    objects = models.Manager()
    valid = utils.ValidCasesManager()

    class Meta:
        """
        Django Meta class.
        """
        managed = False
        db_table = 'cases'
        ordering = ['-term', 'casename']

    def __unicode__(self):
        return self.casename

    def votes(self):
        """
        The typical vote score for this case, e.g., 9-0.
        """
        if self.majvotes and self.minvotes:
            return "%s-%s" % (self.majvotes, self.minvotes)
        return None

    def get_weighted_majvotes(self):
        """
        A scale for weighting the majority votes on a case.
        """
        weighted_votes = (9,8,7,6,0)
        if ((int(self.majvotes) + int(self.minvotes)) < 9):
            """
            We assume missing justices voted with the majority.
            4 minority votes = 0 weighted votes.
            """
            return weighted_votes[int(self.minvotes)]
        return int(self.majvotes)

    def set_weighted_majvotes(self):
        """
        Set the weighted majority votes on this model instance.
        """
        if self.decisiondirection == "1":
            self.weighted_majvotes = self.get_weighted_majvotes
        elif self.decisiondirection == "2":
            self.weighted_majvotes = self.get_weighted_majvotes * -1
        elif self.decisiondirection == "3":
            self.weighted_majvotes = 0

class Justice(utils.BaseScotusModel):
    """
    Represents a single supreme court justice.
    We have justice data from 1946 to present.
    Much of this data is incomplete and will need
    to be hand-edited, e.g., 'current' or the
    various dates for nomination / confirmation.
    """
    justice = models.CharField(max_length=255, primary_key=True)
    justicename = models.CharField(max_length=255, blank=True, null=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    chief_justice = models.NullBooleanField()
    confirmation_votes_for = models.CharField(max_length=255, blank=True, null=True)
    confirmation_votes_against = models.CharField(max_length=255, blank=True, null=True)
    qualifications_score = models.FloatField(blank=True, null=True)
    ideology_score = models.FloatField(blank=True, null=True)

    class Meta:
        """
        Django Meta class.
        """
        managed = False
        db_table = 'scotus_justices'

    def __unicode__(self):
        if self.full_name and self.full_name != '-':
            return self.full_name
        return self.justicename

    def common_cases(self, justices, term=None, naturalcourt=None, maxvotes=None):
        """
        Cases this Justice and all Justices in the list `justices` have in common.
        """
        positions = Vote.objects.all()
        if term:
            positions = positions.filter(term=term)
        if naturalcourt:
            positions = positions.filter(naturalcourt=naturalcourt)
        if maxvotes:
            maxvotes = maxvotes.split(',')
            positions = positions.filter(majvotes__in=maxvotes)
        votes = []
        votes.append(
            set([p['caseid'] for p in positions.filter(justice=self.justice).values('caseid')]))
        for j in justices:
            votes.append(
                set([p['caseid'] for p in positions.filter(justicename=j).values('caseid')]))

        intersecting_cases = votes[0]
        for justice_case in votes[1:]:
            list(intersecting_cases.intersection(justice_case))
        return intersecting_cases

    def agree_positions(self, justices, cc):
        """
        Votes where this Justice and all Justices in the list `justices` were in the majority.
        """
        votes = []
        votes.append(set([p['caseid'] for p in Vote.objects.filter(justice=self.justice, caseid__in=cc, vote__in=['1', '3', '4', '5']).values('caseid')]))

        for j in justices:
            votes.append(set([p['caseid'] for p in Vote.objects.filter(justicename=j, caseid__in=cc, vote__in=['1', '3', '4', '5']).values('caseid')]))

        intersecting_votes = votes[0]
        for vote in votes[1:]:
            intersecting_votes = intersecting_votes.intersection(vote)

        return  (len(list(intersecting_votes)), intersecting_votes)

    def disagree_positions(self, justices, cc):
        """
        Votes where this Justice and all Justices in the list `justices` were in the minority.
        """
        votes = []
        votes.append(set([p['caseid'] for p in Vote.objects.filter(justice=self.justice, caseid__in=cc, vote__in=['2']).values('caseid')]))

        for j in justices:
            votes.append(set([p['caseid'] for p in Vote.objects.filter(justicename=j, caseid__in=cc, vote__in=['2']).values('caseid')]))

        intersecting_votes = votes[0]
        for vote in votes[1:]:
            intersecting_votes = intersecting_votes.intersection(vote)

        return (len(list(intersecting_votes)), intersecting_votes)


class Vote(utils.BaseScotusModel):
    """
    Represents a single justice's position on a single merits
    case. Largely derived from SCDB data, so only for cases from
    1946-present.
    """
    caseid = models.CharField(max_length=255, blank=True, null=True)
    docketid = models.CharField(max_length=255, blank=True, null=True)
    caseissuesid = models.CharField(max_length=255, blank=True, null=True)
    voteid = models.CharField(max_length=255, primary_key=True)
    datedecision = models.CharField(max_length=255, blank=True, null=True)
    decisiontype = models.CharField(max_length=255, blank=True, null=True)
    uscite = models.CharField(max_length=255, blank=True, null=True)
    sctcite = models.CharField(max_length=255, blank=True, null=True)
    ledcite = models.CharField(max_length=255, blank=True, null=True)
    lexiscite = models.CharField(max_length=255, blank=True, null=True)
    term = models.CharField(max_length=255, blank=True, null=True)
    naturalcourt = models.CharField(max_length=255, blank=True, null=True)
    chief = models.CharField(max_length=255, blank=True, null=True)
    docket = models.CharField(max_length=255, blank=True, null=True)
    casename = models.CharField(max_length=255, blank=True, null=True)
    dateargument = models.CharField(max_length=255, blank=True, null=True)
    datereargument = models.CharField(max_length=255, blank=True, null=True)
    petitioner = models.CharField(max_length=255, blank=True, null=True)
    petitionerstate = models.CharField(max_length=255, blank=True, null=True)
    respondent = models.CharField(max_length=255, blank=True, null=True)
    respondentstate = models.CharField(max_length=255, blank=True, null=True)
    jurisdiction = models.CharField(max_length=255, blank=True, null=True)
    adminaction = models.CharField(max_length=255, blank=True, null=True)
    adminactionstate = models.CharField(max_length=255, blank=True, null=True)
    threejudgefdc = models.CharField(max_length=255, blank=True, null=True)
    caseorigin = models.CharField(max_length=255, blank=True, null=True)
    caseoriginstate = models.CharField(max_length=255, blank=True, null=True)
    casesource = models.CharField(max_length=255, blank=True, null=True)
    casesourcestate = models.CharField(max_length=255, blank=True, null=True)
    lcdisagreement = models.CharField(max_length=255, blank=True, null=True)
    certreason = models.CharField(max_length=255, blank=True, null=True)
    lcdisposition = models.CharField(max_length=255, blank=True, null=True)
    lcdispositiondirection = models.CharField(max_length=255, blank=True, null=True)
    declarationuncon = models.CharField(max_length=255, blank=True, null=True)
    casedisposition = models.CharField(max_length=255, blank=True, null=True)
    casedispositionunusual = models.CharField(max_length=255, blank=True, null=True)
    partywinning = models.CharField(max_length=255, blank=True, null=True)
    precedentalteration = models.CharField(max_length=255, blank=True, null=True)
    voteunclear = models.CharField(max_length=255, blank=True, null=True)
    issue = models.CharField(max_length=255, blank=True, null=True)
    issuearea = models.CharField(max_length=255, blank=True, null=True)
    decisiondirection = models.CharField(max_length=255, blank=True, null=True)
    decisiondirectiondissent = models.CharField(max_length=255, blank=True, null=True)
    authoritydecision1 = models.CharField(max_length=255, blank=True, null=True)
    authoritydecision2 = models.CharField(max_length=255, blank=True, null=True)
    lawtype = models.CharField(max_length=255, blank=True, null=True)
    lawsupp = models.CharField(max_length=255, blank=True, null=True)
    lawminor = models.CharField(max_length=255, blank=True, null=True)
    majopinwriter = models.CharField(max_length=255, blank=True, null=True)
    majopinassigner = models.CharField(max_length=255, blank=True, null=True)
    splitvote = models.CharField(max_length=255, blank=True, null=True)
    majvotes = models.CharField(max_length=255, blank=True, null=True)
    minvotes = models.CharField(max_length=255, blank=True, null=True)
    justice = models.CharField(max_length=255, blank=True, null=True)
    justicename = models.CharField(max_length=255, blank=True, null=True)
    vote = models.CharField(max_length=255, blank=True, null=True)
    opinion = models.CharField(max_length=255, blank=True, null=True)
    direction = models.CharField(max_length=255, blank=True, null=True)
    majority = models.CharField(max_length=255, blank=True, null=True)
    firstagreement = models.CharField(max_length=255, blank=True, null=True)
    secondagreement = models.CharField(max_length=255, blank=True, null=True)
    weighted_majvotes = models.IntegerField(blank=True, null=True)
    objects = models.Manager()
    valid = utils.ValidCasesManager()

    class Meta:
        """
        Django Meta class.
        """
        managed = False
        db_table = 'votes'
        ordering = ['-term', 'casename']

    def __unicode__(self):
        return "%s in %s" % (self.justice_obj(), self.case_obj())

    def justice_obj(self):
        """
        Go to the database, get the Justice object.
        """
        if Justice.objects.filter(justice=self.justice).count() == 1:
            return Justice.objects.get(justice=self.justice)
        return self.justice

    def case_obj(self):
        """
        Go to the database, get the Case object.
        """
        if Case.objects.filter(caseid=self.caseid).count() == 1:
            return Case.objects.get(caseid=self.caseid)
        return self.casename

    def is_majority(self):
        """
        Translates self.majority from string values to True/False.
        """
        if self.majority == "1":
            return False
        if self.majority == "2":
            return True
        return None


class JusticeTerm(utils.BaseScotusModel):
    term = models.CharField(max_length=255, blank=True, null=True)
    justice = models.CharField(max_length=255, blank=True, null=True)
    justicename = models.CharField(max_length=255, blank=True, null=True)
    justiceterm = models.CharField(primary_key=True, max_length=255)
    code = models.CharField(max_length=255, blank=True, null=True)
    post_mn = models.FloatField(blank=True, null=True)
    post_sd = models.FloatField(blank=True, null=True)
    post_med = models.FloatField(blank=True, null=True)
    post_025 = models.FloatField(blank=True, null=True)
    post_975 = models.FloatField(blank=True, null=True)

    class Meta:
        """
        Django Meta class.
        """
        managed = False
        db_table = 'justice_terms'
        ordering = ('-term', 'justice')

    def __unicode__(self):
        return "%s (%s)" % (self.justice_obj(), self.term)

    def liberal_pct(self):
        """
        Returns a dictionary of the percentage of liberal votes.
        """
        return {"liberal": len(self.liberal_votes()), "total": len(self.votes()), "pct": len(self.liberal_votes()) / float(len(self.votes()))}

    def justice_obj(self):
        """
        Returns a dictionary of the percentage of liberal votes.
        """
        if Justice.objects.filter(justice=self.justice).count() == 1:
            return Justice.objects.get(justice=self.justice)
        return None

    def justice_dict(self):
        """
        Returns a dictionary for this justice.
        """
        payload = self.dict()
        payload['justice'] = int(self.justice)
        payload['term'] = int(self.term)
        j = self.justice_obj()
        if j:
            payload['justice_data'] = j.dict()
        return payload

    def liberal_votes(self):
        """
        Returns all liberal votes from this term.
        """
        return Vote.valid.filter(justice=self.justice, term=self.term, direction="2")

    def votes(self):
        """
        Returns all votes from this term.
        """
        return Vote.valid.filter(justice=self.justice, term=self.term)
