

(define (problem BW-rand-10)
(:domain BLOCKS)
(:objects b1 b2 b3 b4 b5 b6 b7 b8 b9 b10 - block)
(:init
(handempty)
(on b1 b3)
(on b2 b9)
(ontable b3)
(on b4 b8)
(on b5 b1)
(ontable b6)
(ontable b7)
(on b8 b2)
(on b9 b7)
(ontable b10)
(clear b4)
(clear b5)
(clear b6)
(clear b10)
)
(:goal
(and
(on b1 b7)
(on b2 b10)
(on b3 b6)
(on b5 b8)
(on b7 b2)
(on b8 b3)
(on b9 b4)
(on b10 b9))
)
)


