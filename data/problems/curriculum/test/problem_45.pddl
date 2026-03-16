

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(ontable b1)
(on b2 b5)
(on b3 b2)
(ontable b4)
(on b5 b6)
(ontable b6)
(on b7 b11)
(on b8 b7)
(on b9 b8)
(on b10 b3)
(on b11 b1)
(clear b4)
(clear b9)
(clear b10)
)
(:goal
(and
(on b1 b11)
(on b2 b6)
(on b3 b2)
(on b5 b10)
(on b6 b8)
(on b7 b4)
(on b8 b7)
(on b10 b3))
)
)


