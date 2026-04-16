(set-logic ALL)
; Constraint ID: 08cd60fea2bb349a
; Generated at: 2026-04-16 11:43:57
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60298)) (False)
(assert (not (= x 60298)))

; Query: ((== x 60299)) (False)
(assert (not (not (= x 60299))))

(check-sat)
(get-model)
