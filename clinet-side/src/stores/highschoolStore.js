import { defineStore } from 'pinia';

export const useHighSchoolStore = defineStore('highSchoolStore', {
  state: () => ({
    highSchools: 
    [
        {
          "highSchool": "Ankara Fen Lisesi",
          "yksAverage": 480,
          "studentsToBilkent": 50,
          "fullScholarship": 30,
          "halfScholarship": 15,
          "noScholarship": 5,
          "visitsToBilkent": 5,
          "visitingStudents": 200
        },
        {
          "highSchool": "İstanbul Erkek Lisesi",
          "yksAverage": 475,
          "studentsToBilkent": 45,
          "fullScholarship": 25,
          "halfScholarship": 15,
          "noScholarship": 5,
          "visitsToBilkent": 4,
          "visitingStudents": 180
        },
        {
          "highSchool": "Bornova Anadolu Lisesi",
          "yksAverage": 465,
          "studentsToBilkent": 40,
          "fullScholarship": 20,
          "halfScholarship": 10,
          "noScholarship": 10,
          "visitsToBilkent": 4,
          "visitingStudents": 150
        },
        {
          "highSchool": "Kadıköy Anadolu Lisesi",
          "yksAverage": 460,
          "studentsToBilkent": 60,
          "fullScholarship": 10,
          "halfScholarship": 20,
          "noScholarship": 30,
          "visitsToBilkent": 6,
          "visitingStudents": 220
        },
        {
          "highSchool": "Galatasaray Lisesi",
          "yksAverage": 470,
          "studentsToBilkent": 38,
          "fullScholarship": 18,
          "halfScholarship": 15,
          "noScholarship": 5,
          "visitsToBilkent": 3,
          "visitingStudents": 160
        },
        {
          "highSchool": "Kabataş Erkek Lisesi",
          "yksAverage": 450,
          "studentsToBilkent": 35,
          "fullScholarship": 10,
          "halfScholarship": 15,
          "noScholarship": 10,
          "visitsToBilkent": 4,
          "visitingStudents": 140
        },
        {
          "highSchool": "İzmir Fen Lisesi",
          "yksAverage": 490,
          "studentsToBilkent": 15,
          "fullScholarship": 10,
          "halfScholarship": 4,
          "noScholarship": 1,
          "visitsToBilkent": 3,
          "visitingStudents": 100
        },
        {
          "highSchool": "Robert Koleji",
          "yksAverage": 495,
          "studentsToBilkent": 10,
          "fullScholarship": 6,
          "halfScholarship": 3,
          "noScholarship": 1,
          "visitsToBilkent": 2,
          "visitingStudents": 80
        },
        {
          "highSchool": "TED Ankara Koleji",
          "yksAverage": 440,
          "studentsToBilkent": 50,
          "fullScholarship": 5,
          "halfScholarship": 15,
          "noScholarship": 30,
          "visitsToBilkent": 5,
          "visitingStudents": 210
        },
        {
          "highSchool": "Üsküdar Amerikan Lisesi",
          "yksAverage": 475,
          "studentsToBilkent": 30,
          "fullScholarship": 10,
          "halfScholarship": 15,
          "noScholarship": 5,
          "visitsToBilkent": 4,
          "visitingStudents": 140
        },
        {
          "highSchool": "Adana Fen Lisesi",
          "yksAverage": 465,
          "studentsToBilkent": 20,
          "fullScholarship": 8,
          "halfScholarship": 6,
          "noScholarship": 6,
          "visitsToBilkent": 3,
          "visitingStudents": 100
        },
        {
          "highSchool": "İzmir Amerikan Koleji",
          "yksAverage": 480,
          "studentsToBilkent": 25,
          "fullScholarship": 15,
          "halfScholarship": 5,
          "noScholarship": 5,
          "visitsToBilkent": 3,
          "visitingStudents": 110
        },
        {
          "highSchool": "Eskişehir Anadolu Lisesi",
          "yksAverage": 430,
          "studentsToBilkent": 40,
          "fullScholarship": 5,
          "halfScholarship": 10,
          "noScholarship": 25,
          "visitsToBilkent": 3,
          "visitingStudents": 150
        },
        {
          "highSchool": "Antalya Fen Lisesi",
          "yksAverage": 470,
          "studentsToBilkent": 22,
          "fullScholarship": 12,
          "halfScholarship": 8,
          "noScholarship": 2,
          "visitsToBilkent": 2,
          "visitingStudents": 100
        },
        {
          "highSchool": "Beşiktaş Anadolu Lisesi",
          "yksAverage": 445,
          "studentsToBilkent": 30,
          "fullScholarship": 5,
          "halfScholarship": 10,
          "noScholarship": 15,
          "visitsToBilkent": 4,
          "visitingStudents": 120
        },
        {
          "highSchool": "Samsun Fen Lisesi",
          "yksAverage": 450,
          "studentsToBilkent": 25,
          "fullScholarship": 8,
          "halfScholarship": 10,
          "noScholarship": 7,
          "visitsToBilkent": 3,
          "visitingStudents": 110
        },
        {
          "highSchool": "Mersin Fen Lisesi",
          "yksAverage": 470,
          "studentsToBilkent": 20,
          "fullScholarship": 10,
          "halfScholarship": 7,
          "noScholarship": 3,
          "visitsToBilkent": 2,
          "visitingStudents": 100
        },
        {
          "highSchool": "Konya Anadolu Lisesi",
          "yksAverage": 435,
          "studentsToBilkent": 35,
          "fullScholarship": 5,
          "halfScholarship": 10,
          "noScholarship": 20,
          "visitsToBilkent": 3,
          "visitingStudents": 140
        },
        {
          "highSchool": "Malatya Fen Lisesi",
          "yksAverage": 455,
          "studentsToBilkent": 18,
          "fullScholarship": 7,
          "halfScholarship": 6,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 90
        },
        {
          "highSchool": "Trabzon Fen Lisesi",
          "yksAverage": 460,
          "studentsToBilkent": 19,
          "fullScholarship": 8,
          "halfScholarship": 7,
          "noScholarship": 4,
          "visitsToBilkent": 3,
          "visitingStudents": 100
        },
        {
          "highSchool": "Çankaya Anadolu Lisesi",
          "yksAverage": 440,
          "studentsToBilkent": 28,
          "fullScholarship": 5,
          "halfScholarship": 10,
          "noScholarship": 13,
          "visitsToBilkent": 3,
          "visitingStudents": 120
        },
        {
          "highSchool": "Kocaeli Fen Lisesi",
          "yksAverage": 450,
          "studentsToBilkent": 20,
          "fullScholarship": 10,
          "halfScholarship": 5,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 90
        },
        {
          "highSchool": "İstanbul Amerikan Robert Koleji",
          "yksAverage": 495,
          "studentsToBilkent": 10,
          "fullScholarship": 8,
          "halfScholarship": 2,
          "noScholarship": 0,
          "visitsToBilkent": 1,
          "visitingStudents": 50
        },
        {
          "highSchool": "Edirne Fen Lisesi",
          "yksAverage": 465,
          "studentsToBilkent": 16,
          "fullScholarship": 6,
          "halfScholarship": 6,
          "noScholarship": 4,
          "visitsToBilkent": 2,
          "visitingStudents": 80
        },
        {
          "highSchool": "Bursa Anadolu Lisesi",
          "yksAverage": 440,
          "studentsToBilkent": 30,
          "fullScholarship": 5,
          "halfScholarship": 10,
          "noScholarship": 15,
          "visitsToBilkent": 4,
          "visitingStudents": 120
        },
        {
          "highSchool": "İstanbul Pendik Anadolu Lisesi",
          "yksAverage": 390,
          "studentsToBilkent": 15,
          "fullScholarship": 1,
          "halfScholarship": 5,
          "noScholarship": 9,
          "visitsToBilkent": 2,
          "visitingStudents": 50
        },
        {
          "highSchool": "Adana Anadolu Lisesi",
          "yksAverage": 375,
          "studentsToBilkent": 10,
          "fullScholarship": 1,
          "halfScholarship": 4,
          "noScholarship": 5,
          "visitsToBilkent": 1,
          "visitingStudents": 30
        },
        {
          "highSchool": "Gaziantep Anadolu Lisesi",
          "yksAverage": 365,
          "studentsToBilkent": 8,
          "fullScholarship": 0,
          "halfScholarship": 3,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 40
        },
        {
          "highSchool": "Sivas Anadolu Lisesi",
          "yksAverage": 370,
          "studentsToBilkent": 12,
          "fullScholarship": 2,
          "halfScholarship": 5,
          "noScholarship": 5,
          "visitsToBilkent": 3,
          "visitingStudents": 60
        },
        {
          "highSchool": "Mardin Anadolu Lisesi",
          "yksAverage": 350,
          "studentsToBilkent": 5,
          "fullScholarship": 0,
          "halfScholarship": 2,
          "noScholarship": 3,
          "visitsToBilkent": 1,
          "visitingStudents": 20
        },
        {
          "highSchool": "Erzurum Anadolu Lisesi",
          "yksAverage": 360,
          "studentsToBilkent": 6,
          "fullScholarship": 1,
          "halfScholarship": 2,
          "noScholarship": 3,
          "visitsToBilkent": 1,
          "visitingStudents": 25
        },
        {
          "highSchool": "Şanlıurfa Anadolu Lisesi",
          "yksAverage": 340,
          "studentsToBilkent": 4,
          "fullScholarship": 0,
          "halfScholarship": 1,
          "noScholarship": 3,
          "visitsToBilkent": 1,
          "visitingStudents": 15
        },
        {
          "highSchool": "Kars Anadolu Lisesi",
          "yksAverage": 330,
          "studentsToBilkent": 3,
          "fullScholarship": 0,
          "halfScholarship": 1,
          "noScholarship": 2,
          "visitsToBilkent": 1,
          "visitingStudents": 10
        },
        {
          "highSchool": "Van Anadolu Lisesi",
          "yksAverage": 355,
          "studentsToBilkent": 7,
          "fullScholarship": 1,
          "halfScholarship": 2,
          "noScholarship": 4,
          "visitsToBilkent": 1,
          "visitingStudents": 25
        },
        {
          "highSchool": "Diyarbakır Anadolu Lisesi",
          "yksAverage": 365,
          "studentsToBilkent": 9,
          "fullScholarship": 1,
          "halfScholarship": 3,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 35
        },
        {
          "highSchool": "Malatya Anadolu Lisesi",
          "yksAverage": 380,
          "studentsToBilkent": 10,
          "fullScholarship": 2,
          "halfScholarship": 3,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 40
        },
        {
          "highSchool": "Kayseri Anadolu Lisesi",
          "yksAverage": 395,
          "studentsToBilkent": 20,
          "fullScholarship": 2,
          "halfScholarship": 5,
          "noScholarship": 13,
          "visitsToBilkent": 3,
          "visitingStudents": 60
        },
        {
          "highSchool": "Bolu Fen Lisesi",
          "yksAverage": 400,
          "studentsToBilkent": 15,
          "fullScholarship": 5,
          "halfScholarship": 5,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 45
        },
        {
          "highSchool": "Tekirdağ Anadolu Lisesi",
          "yksAverage": 370,
          "studentsToBilkent": 8,
          "fullScholarship": 1,
          "halfScholarship": 3,
          "noScholarship": 4,
          "visitsToBilkent": 1,
          "visitingStudents": 20
        },
        {
          "highSchool": "Kahramanmaraş Anadolu Lisesi",
          "yksAverage": 380,
          "studentsToBilkent": 9,
          "fullScholarship": 1,
          "halfScholarship": 4,
          "noScholarship": 4,
          "visitsToBilkent": 2,
          "visitingStudents": 30
        },
        {
          "highSchool": "Trabzon Anadolu Lisesi",
          "yksAverage": 360,
          "studentsToBilkent": 7,
          "fullScholarship": 0,
          "halfScholarship": 3,
          "noScholarship": 4,
          "visitsToBilkent": 1,
          "visitingStudents": 25
        },
        {
          "highSchool": "Balıkesir Anadolu Lisesi",
          "yksAverage": 375,
          "studentsToBilkent": 12,
          "fullScholarship": 2,
          "halfScholarship": 4,
          "noScholarship": 6,
          "visitsToBilkent": 2,
          "visitingStudents": 35
        },
        {
          "highSchool": "Çanakkale Fen Lisesi",
          "yksAverage": 405,
          "studentsToBilkent": 18,
          "fullScholarship": 5,
          "halfScholarship": 5,
          "noScholarship": 8,
          "visitsToBilkent": 2,
          "visitingStudents": 50
        },
        {
          "highSchool": "Hatay Anadolu Lisesi",
          "yksAverage": 370,
          "studentsToBilkent": 8,
          "fullScholarship": 1,
          "halfScholarship": 3,
          "noScholarship": 4,
          "visitsToBilkent": 1,
          "visitingStudents": 20
        },
        {
          "highSchool": "Osmaniye Fen Lisesi",
          "yksAverage": 360,
          "studentsToBilkent": 5,
          "fullScholarship": 0,
          "halfScholarship": 2,
          "noScholarship": 3,
          "visitsToBilkent": 1,
          "visitingStudents": 15
        },
        {
          "highSchool": "Zonguldak Anadolu Lisesi",
          "yksAverage": 365,
          "studentsToBilkent": 9,
          "fullScholarship": 1,
          "halfScholarship": 3,
          "noScholarship": 5,
          "visitsToBilkent": 1,
          "visitingStudents": 30
        },
        {
          "highSchool": "Manisa Anadolu Lisesi",
          "yksAverage": 380,
          "studentsToBilkent": 11,
          "fullScholarship": 2,
          "halfScholarship": 4,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 35
        },
        {
          "highSchool": "Edirne Anadolu Lisesi",
          "yksAverage": 370,
          "studentsToBilkent": 10,
          "fullScholarship": 1,
          "halfScholarship": 4,
          "noScholarship": 5,
          "visitsToBilkent": 2,
          "visitingStudents": 30
        },
        {
          "highSchool": "Karabük Fen Lisesi",
          "yksAverage": 360,
          "studentsToBilkent": 6,
          "fullScholarship": 0,
          "halfScholarship": 2,
          "noScholarship": 4,
          "visitsToBilkent": 1,
          "visitingStudents": 20
        },
        {
          "highSchool": "Kırklareli Anadolu Lisesi",
          "yksAverage": 370,
          "studentsToBilkent": 7,
          "fullScholarship": 1,
          "halfScholarship": 3,
          "noScholarship": 3,
          "visitsToBilkent": 1,
          "visitingStudents": 25
        }
      ]
      ,
  }),
  getters: {
    sortedByYksAverage: (state) =>
      state.highSchools.sort((a, b) => b.yksAverage - a.yksAverage),
    totalVisits: (state) =>
      state.highSchools.reduce((total, hs) => total + hs.visitsToBilkent, 0),
    totalStudentsSent: (state) =>
      state.highSchools.reduce(
        (total, hs) => total + hs.studentsToBilkent,
        0
      ),
  },
  actions: {
    addHighSchool(data) {
      this.highSchools.push(data);
    },
    removeHighSchool(highSchoolName) {
      this.highSchools = this.highSchools.filter(
        (hs) => hs.highSchool !== highSchoolName
      );
    },
  },
});
