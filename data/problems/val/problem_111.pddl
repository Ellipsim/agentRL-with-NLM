

(define (problem BW-rand-11)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 - block)
(:init
(handempty)
(on b1 b8)
(ontable b2)
(ontable b3)
(on b4 b3)
(on b5 b11)
(on b6 b10)
(on b7 b9)
(ontable b8)
(on b9 b4)
(on b10 b1)
(ontable b11)
(clear b2)
(clear b5)
(clear b6)
(clear b7)
)
(:goal
(and
(on b1 b8)
(on b2 b9)
(on b3 b1)
(on b5 b6)
(on b6 b4)
(on b7 b3)
(on b9 b11)
(on b11 b5))
)
)


