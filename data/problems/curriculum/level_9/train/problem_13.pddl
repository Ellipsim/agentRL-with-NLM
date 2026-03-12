

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b5)
(on b2 b11)
(on b3 b6)
(on b4 b3)
(on-table b5)
(on b6 b10)
(on-table b7)
(on b8 b9)
(on-table b9)
(on b10 b1)
(on b11 b8)
(clear b2)
(clear b4)
(clear b7)
)
(:goal
(and
(on b1 b9)
(on b2 b6)
(on b3 b8)
(on b4 b10)
(on b7 b3)
(on b8 b2)
(on b9 b7)
(on b10 b5)
(on b11 b4))
)
)


