(set-logic ALL)
; Constraint ID: ab3548955f43d130
; Generated at: 2026-04-16 11:29:08
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59992)) (False)
(assert (not (= x 59992)))

; Query: ((== x 59993)) (False)
(assert (not (not (= x 59993))))

(check-sat)
(get-model)
