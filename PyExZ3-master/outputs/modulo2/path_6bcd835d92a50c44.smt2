(set-logic ALL)
; Executed Path ID: 6bcd835d92a50c44
; Generated at: 2026-04-17 03:12:54
; Solver: Z3Wrapper
; Number of predicates: 3
; Has query: False

(declare-const in1 Int)

; ((<= in1 0)) (False)
(assert (not (<= in1 0)))
; ((!= (% in1 3) 0)) (False)
(assert (not (not (= (mod in1 3) 0))))
; ((!= (% in1 5) 0)) (False)
(assert (not (not (= (mod in1 5) 0))))

(check-sat)
(get-model)
