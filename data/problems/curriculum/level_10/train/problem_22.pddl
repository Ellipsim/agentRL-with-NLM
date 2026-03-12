

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b3)
(on b3 b8)
(on-table b4)
(on b5 b2)
(on-table b6)
(on b7 b11)
(on b8 b10)
(on-table b9)
(on b10 b4)
(on b11 b6)
(clear b1)
(clear b7)
(clear b9)
)
(:goal
(and
(on b1 b11)
(on b2 b8)
(on b4 b3)
(on b6 b7)
(on b7 b9)
(on b9 b10)
(on b10 b4)
(on b11 b6))
)
)


