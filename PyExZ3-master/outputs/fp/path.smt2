(set-logic ALL)
; Path ID: e9dedf9dce3a164d
; Generated at: 2026-04-16 12:01:25
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const a Int)
(declare-const se Int)

; ((== (% a 2) 0)) (True)
(assert (= % 0))

; Query: ((== a 1)) (False)
(assert (not (not (= a 1))))

(check-sat)
(get-model)
