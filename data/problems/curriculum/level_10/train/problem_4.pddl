

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b10)
(on b2 b9)
(on b3 b4)
(on b4 b7)
(on-table b5)
(on b6 b5)
(on b7 b6)
(on b8 b11)
(on b9 b1)
(on-table b10)
(on b11 b2)
(clear b3)
(clear b8)
)
(:goal
(and
(on b1 b5)
(on b2 b8)
(on b3 b1)
(on b5 b2)
(on b6 b4)
(on b7 b10)
(on b9 b7)
(on b10 b11)
(on b11 b6))
)
)


