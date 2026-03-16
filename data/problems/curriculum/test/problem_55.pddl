

(define (problem BW-rand-12)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 b11 b12 - block)
(:init
(handempty)
(ontable b1)
(ontable b2)
(on b3 b9)
(on b4 b10)
(on b5 b6)
(on b6 b8)
(ontable b7)
(on b8 b12)
(on b9 b11)
(on b10 b1)
(on b11 b4)
(ontable b12)
(clear b2)
(clear b3)
(clear b5)
(clear b7)
)
(:goal
(and
(on b1 b2)
(on b2 b9)
(on b3 b8)
(on b4 b11)
(on b5 b6)
(on b9 b10)
(on b10 b3)
(on b12 b4))
)
)


