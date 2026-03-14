

(define (problem BW-rand-11)
(:domain blocksworld-4ops)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 )
(:init
(arm-empty)
(on b1 b9)
(on-table b2)
(on b3 b2)
(on-table b4)
(on b5 b11)
(on b6 b3)
(on b7 b10)
(on b8 b4)
(on b9 b5)
(on b10 b8)
(on b11 b6)
(clear b1)
(clear b7)
)
(:goal
(and
(on b2 b4)
(on b3 b5)
(on b6 b11)
(on b10 b9))
)
)


