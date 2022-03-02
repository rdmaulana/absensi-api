from app import ma

class HistoryAbsenPegawaiAll(ma.Schema):
    class Meta:
        fields = (
            'idUser', 
            'namaLengkap',
            'tglAbsensi',
            'jamMasuk',
            'jamKeluar',
            'namaStatus'
        )

class HistoryAbsenPegawai(ma.Schema):
    class Meta:
        fields = (
            'tglAbsensi',
            'jamMasuk',
            'jamKeluar',
            'namaStatus'
        )

history_absensi_all_schema = HistoryAbsenPegawaiAll(many=True)
history_absensi_schema = HistoryAbsenPegawai(many=True)
