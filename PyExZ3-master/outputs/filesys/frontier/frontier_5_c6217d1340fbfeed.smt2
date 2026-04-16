(set-logic ALL)
; Constraint ID: c6217d1340fbfeed
; Generated at: 2026-04-16 11:00:46
; Solver: Z3Wrapper
; Number of assertions: 1
; Has query: True

(declare-const se Int)
(declare-const x Int)

; ((== x 59617)) (False)
(assert (not (= x 59617)))

; Query: ((== x 59618)) (False)
(assert (not (not (= x 59618))))

(check-sat)
(get-model)
