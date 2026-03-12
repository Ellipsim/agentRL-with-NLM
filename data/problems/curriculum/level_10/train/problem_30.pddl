

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on-table b1)
(on b2 b9)
(on b3 b11)
(on-table b4)
(on b5 b8)
(on b6 b4)
(on b7 b5)
(on b8 b1)
(on-table b9)
(on-table b10)
(on b11 b6)
(clear b2)
(clear b3)
(clear b7)
(clear b10)
)
(:goal
(and
(on b1 b9)
(on b2 b6)
(on b3 b5)
(on b4 b1)
(on b6 b3)
(on b7 b4)
(on b8 b11)
(on b10 b7)
(on b11 b2))
)
)


