(set-logic ALL)
; Constraint ID: 156c96638280ed76
; Generated at: 2026-04-16 11:31:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 60073)) (False)
(assert (not (= x 60073)))

; Query: ((== x 60074)) (False)
(assert (not (not (= x 60074))))

(check-sat)
(get-model)
