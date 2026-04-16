(set-logic ALL)
; Executed Path ID: f9742c50a59fe604
; Generated at: 2026-04-16 16:03:01
; Solver: Z3Wrapper
; Number of predicates: 2
; Has query: False

(declare-const in1 Int)

; ((!= (% in1 3) 0)) (False)
(assert (not (not (= (mod in1 3) 0))))
; ((!= (% in1 5) 0)) (True)
(assert (not (= (mod in1 5) 0)))

(check-sat)
(get-model)
