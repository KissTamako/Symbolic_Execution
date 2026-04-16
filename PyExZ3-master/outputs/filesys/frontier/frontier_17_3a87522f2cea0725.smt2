(set-logic ALL)
; Constraint ID: 3a87522f2cea0725
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59635)) (False)
(assert (not (= x 59635)))

; Query: ((== x 59636)) (False)
(assert (not (not (= x 59636))))

(check-sat)
(get-model)
