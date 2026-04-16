(set-logic ALL)
; Constraint ID: 006aec4efce916b3
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60301)) (False)
(assert (not (= x 60301)))

; Query: ((== x 60302)) (False)
(assert (not (not (= x 60302))))

(check-sat)
(get-model)
