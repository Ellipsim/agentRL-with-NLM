

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b6)
(on b2 b9)
(on b3 b4)
(on b4 b7)
(on-table b5)
(on b6 b3)
(on b7 b10)
(on-table b8)
(on b9 b1)
(on b10 b5)
(on b11 b2)
(clear b8)
(clear b11)
)
(:goal
(and
(on b1 b9)
(on b2 b1)
(on b4 b11)
(on b5 b7)
(on b6 b3)
(on b7 b6)
(on b8 b4)
(on b10 b8)
(on b11 b2))
)
)


